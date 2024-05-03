import copy
import math
import numpy as np
import os
import pathlib
import quant
import torch
import torch.nn.functional as F
from quant.football.models import get_model
from quant.football.transforms import get_table_factory
from quant.utils.archive import extract_tar
from quant.utils.io import make_dir, load_json


class FootballInferencer:

    def __init__(self, model_archive, device="cuda"):
        if device == "cuda" and torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

        infer_cfg, cache_dir = self._load_config(model_archive)

        model = self._init_model(infer_cfg["model"], cache_dir / "best.pt")
        model = model.to(device)
        model.eval()

        table_factory = get_table_factory(infer_cfg["table"])

        trial_id = infer_cfg["model"]["log"]["out_dir"]

        self.model = model
        self.device = device
        self.table_factory = table_factory
        self.filter_rules = infer_cfg["filters"]
        self.preprocess_args = infer_cfg["preprocess"]
        self.postprocess_kwargs = infer_cfg["postprocess"]
        self.model_id = f"(v{quant.__version__})" + trial_id

    def _load_config(self, model_archive):
        model_archive = pathlib.Path(model_archive)  # tarfile
        cache_dir = make_dir(f".cache/{os.getpid()}_{model_archive.stem}", exist_ok=False)

        extract_tar(model_archive, cache_dir)

        cfg_files = list(cache_dir.glob("**/infer.json"))
        assert cfg_files, "You must provide a `infer.json` file."

        cache_dir = cfg_files[0].parent

        infer_cfg = load_json(cache_dir / "infer.json")

        # filters: 规则序列, preprocess: 参数序列, model: 配置字典, postprocess: 参数字典
        for key in ["filters", "preprocess", "model", "postprocess"]:
            if isinstance(infer_cfg[key], str):
                infer_cfg[key] = load_json(cache_dir / infer_cfg[key])

        return infer_cfg, cache_dir

    def _init_model(self, model_cfg, weights_file):
        model_cfg = copy.deepcopy(model_cfg["model"])

        model_type = model_cfg.pop("type")
        model = get_model(model_type, **model_cfg)

        model.load_state_dict(torch.load(weights_file, map_location=torch.device("cpu")))

        return model

    def __call__(self, section):
        x, _, z = self.preprocess(section)
        probs = self.forward(x)

        z_base = z[-1]
        if z_base > 0:
            probs = [0] * z_base + probs

        z_score = z[-5]
        assert np.argmax(probs) >= z_score, "The prediction violates the logic of the world."

        bets = section["bets"]["bets"]
        ret_bets = self.postprocess(probs, bets)
        return ret_bets

    def is_valid(self, section):
        filter_rules = self.filter_rules

        for rule in filter_rules:
            rule_name = rule["name"]
            if rule_name == "time_range":
                time_mini, time_maxi = rule["value"]
                game_time = section["game_time"]
                if game_time < time_mini or game_time > time_maxi:
                    return False

        return True

    def preprocess(self, section):
        device = self.device
        args = self.preprocess_args

        sample = self.table_factory.extract_features(section)

        table_name = self.table_factory.table_name
        if table_name in ["table20240326", "table20240414"]:
            # data, stages, encoder, whole, nc, transforms, prediction_method
            X, Y, Z = self.table_factory.export_dataset([sample], *args)[:3]
        elif table_name in ["table20240419", "table20240420"]:
            # data, points, lbacks, encoder, whole, nc, transforms, prediction_method
            curr_time = section["curr_time"]
            X, Y, Z = self.table_factory.export_dataset([sample], [curr_time], *args)[:3]
        else:
            raise NotImplementedError(f"Not supported <{table_name=}>.")

        assert len(X) > 0, "This match contains invalid features."

        x, y, z = X[0], Y[0], Z[0]

        model_class_name = self.model.class_name
        if model_class_name == "STNetV3":
            x_home = torch.tensor([x[0]], dtype=torch.int).to(device)
            x_away = torch.tensor([x[1]], dtype=torch.int).to(device)
            x_features = torch.tensor([x[2:]], dtype=torch.float).to(device)
            x = (x_home, x_away, x_features)
        elif model_class_name == "STNetV4":
            x_season = torch.tensor([x[0]], dtype=torch.int).to(device)
            x_home = torch.tensor([x[1]], dtype=torch.int).to(device)
            x_away = torch.tensor([x[2]], dtype=torch.int).to(device)
            x_features = torch.tensor([x[3:]], dtype=torch.float).to(device)
            x = (x_season, x_home, x_away, x_features)
        else:
            raise NotImplementedError(f"Not supported <{model_class_name=}>.")

        return x, y, z

    @torch.no_grad()
    def forward(self, x):
        output = self.model(x)[0]
        probs = F.softmax(output, dim=-1).tolist()
        return probs

    def postprocess(self, probs, bets):
        # N: ['total', 'total_asian', ...]
        # CP: {0: '全场', 1: '上半场', 2: '下半场'}
        # P: 盘口; E: 方向; C: 赔率
        kwargs = self.postprocess_kwargs

        bet_n_ins = set(kwargs["bet_n_ins"])
        bet_cp_ins = set(kwargs["bet_cp_ins"])
        ret_thr = kwargs["ret_thr"]
        ret_conf_thr = kwargs["ret_conf_thr"]

        ret_bets = []
        for bet in bets:
            bet_n = bet["N"]
            if bet_n not in bet_n_ins:
                continue

            bet_cp = bet["CP"]
            if bet_cp not in bet_cp_ins:
                continue

            bet_p = bet["P"]
            bet_e = bet["E"]
            bet_c = bet["C"]

            _id = int(bet_p + 0.01)
            if math.isclose(bet_p, _id + 0.0, rel_tol=1e-3, abs_tol=0.01):
                conf_gt, conf_lt = sum(probs[_id + 1:]), sum(probs[:_id])

                ret, ret_conf = self._ret_overunder(bet_e, bet_c, conf_gt, conf_lt)
            elif math.isclose(bet_p, _id + 0.25, rel_tol=1e-3, abs_tol=0.01):
                conf_gt, conf_lt = sum(probs[_id + 1:]), sum(probs[:_id])
                ret1, ret_conf1 = self._ret_overunder(bet_e, bet_c, conf_gt, conf_lt)
                conf_gt, conf_lt = sum(probs[_id + 1:]), sum(probs[:_id + 1])
                ret2, ret_conf2 = self._ret_overunder(bet_e, bet_c, conf_gt, conf_lt)

                ret, ret_conf = (ret1 + ret2) * 0.5, (ret_conf1 + ret_conf2) * 0.5
            elif math.isclose(bet_p, _id + 0.50, rel_tol=1e-3, abs_tol=0.01):
                conf_gt, conf_lt = sum(probs[_id + 1:]), sum(probs[:_id + 1])

                ret, ret_conf = self._ret_overunder(bet_e, bet_c, conf_gt, conf_lt)
            elif math.isclose(bet_p, _id + 0.75, rel_tol=1e-3, abs_tol=0.01):
                conf_gt, conf_lt = sum(probs[_id + 1:]), sum(probs[:_id + 1])
                ret1, ret_conf1 = self._ret_overunder(bet_e, bet_c, conf_gt, conf_lt)
                conf_gt, conf_lt = sum(probs[_id + 2:]), sum(probs[:_id + 1])
                ret2, ret_conf2 = self._ret_overunder(bet_e, bet_c, conf_gt, conf_lt)

                ret, ret_conf = (ret1 + ret2) * 0.5, (ret_conf1 + ret_conf2) * 0.5
            else:
                continue

            if ret >= ret_thr and ret_conf >= ret_conf_thr:
                bet = copy.deepcopy(bet)
                bet["return"] = ret
                bet["confidence"] = ret_conf
                bet["model_id"] = self.model_id
                ret_bets.append(bet)

        return ret_bets

    def _ret_overunder(self, bet_e, bet_c, conf_gt, conf_lt):
        conf_eq = 1.0 - conf_gt - conf_lt

        if bet_e == "over":
            ret = conf_eq + conf_gt * bet_c - conf_lt
            ret_conf = conf_eq + conf_gt
        elif bet_e == "under":
            ret = conf_eq + conf_lt * bet_c - conf_gt
            ret_conf = conf_eq + conf_lt
        else:
            ret, ret_conf = 0.0, 0.0

        return ret, ret_conf
