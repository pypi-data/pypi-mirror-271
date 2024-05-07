import sys
import torch
import torch.nn.functional as F
from pathlib import Path
from quant.football.models import get_model
from quant.utils.io import load_json, load_pkl, save_pkl


def load_model(model_cfg, checkpoint):
    model_type = model_cfg.pop("type")
    model = get_model(model_type, **model_cfg)

    model.load_state_dict(torch.load(checkpoint, map_location=torch.device("cpu")))

    return model


def test_dataset(test_file, checkpoint_dir, out_file=None, device="cuda"):
    if device == "cuda" and torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    checkpoint_dir = Path(checkpoint_dir)
    model_cfg = load_json(checkpoint_dir / "model.json")
    model = load_model(model_cfg["model"], checkpoint_dir / "best.pt")
    model = model.to(device)
    model.eval()

    results, correct = [], 0

    suffix = Path(test_file).suffix
    if suffix == ".json":
        X, Y, Z = load_json(test_file)[:3]
    elif suffix == ".pkl":
        X, Y, Z = load_pkl(test_file)[:3]
    else:
        raise NotImplementedError(f"Not supported <{suffix=}>.")

    with torch.no_grad():
        model_class_name = model.class_name
        for x, y, z in zip(X, Y, Z):
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

            output = model(x)[0]
            y_ = output.argmax().item()
            probs = F.softmax(output, dim=-1).tolist()

            results.append([y, z, y_, probs])
            if y == y_:
                correct += 1

    dataset_size = len(results)
    test_acc = correct / dataset_size
    print(f"\nAcc: {correct}/{dataset_size} ({test_acc:.4f})\n")

    if out_file is not None:
        save_pkl(out_file, results)

    return results, test_acc


if __name__ == "__main__":
    kwargs = {
        "out_file": None,
        "device": "cuda",
    }
    for arg in sys.argv[1:]:
        key, value = arg.split("=", maxsplit=1)
        kwargs[key] = value

    test_dataset(**kwargs)
