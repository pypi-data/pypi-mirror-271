import argparse
import pathlib
import sys
import time

import nni
import quant.core.builders as builders
import quant.core.config as config
import quant.core.distributed as dist
import quant.core.net as net
import quant.core.trainer as trainer
from quant.core.config import cfg


def parse_args():
    """Parse command line options (mode and config)."""
    parser = argparse.ArgumentParser(description="Run a model.")
    help_s, choices = "Run mode", ["info", "train", "test", "time"]
    parser.add_argument("--mode", help=help_s, choices=choices, required=True, type=str)
    help_s = "Config file location"
    parser.add_argument("--cfg", help=help_s, required=True, type=str)
    help_s = "See quant/core/config.py for all options"
    parser.add_argument("opts", help=help_s, default=None, nargs=argparse.REMAINDER)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main():
    """Execute operation (train, test, time, etc.)."""
    args = parse_args()
    mode = args.mode
    config.load_cfg(args.cfg)
    cfg.merge_from_list(args.opts)
    trial_name = time.strftime("%Y%m%d") + f"_{nni.get_experiment_id()}_{nni.get_sequence_id():04d}"
    cfg.OUT_DIR = str(pathlib.Path(cfg.OUT_DIR) / trial_name)
    optimized_params = nni.get_next_parameter()
    cfg.merge_from_list([item for pair in optimized_params.items() for item in pair])
    config.assert_cfg()
    cfg.freeze()
    if mode == "info":
        print(builders.get_model()())
        print("complexity:", net.complexity(builders.get_model()))
    elif mode == "train":
        dist.multi_proc_run(num_proc=cfg.NUM_GPUS, fun=trainer.train_model)
    elif mode == "test":
        dist.multi_proc_run(num_proc=cfg.NUM_GPUS, fun=trainer.test_model)


if __name__ == "__main__":
    main()
