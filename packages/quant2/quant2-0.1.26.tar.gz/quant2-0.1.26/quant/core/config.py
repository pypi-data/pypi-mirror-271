import os

from quant.core.io import pathmgr
from yacs.config import CfgNode


# Global config object (example usage: from core.config import cfg)
_C = CfgNode()
cfg = _C


# ---------------------------------- Model options ----------------------------------- #
_C.MODEL = CfgNode()

# Model type
_C.MODEL.TYPE = ""

# Number of input channels. Default: 3
_C.MODEL.IN_CHANS = 3

# Number of classes
_C.MODEL.NUM_CLASSES = 10

# Loss function (see models/loss.py for options)
_C.MODEL.LOSS_FUN = "cross_entropy"

# Activation function (relu or silu/swish)
_C.MODEL.ACTIVATION_FUN = "relu"

# Perform activation inplace if implemented
_C.MODEL.ACTIVATION_INPLACE = True


# ---------------------------------- NpzNet options ---------------------------------- #
_C.NPZNET = CfgNode(new_allowed=True)

# Stem conv kernel size
_C.NPZNET.STEM_KERNEL = 4

# Stem conv stride
_C.NPZNET.STEM_STRIDE = 4

# Number of blocks at each stage. Default: [3, 3, 9, 3]
_C.NPZNET.DEPTHS = [3, 3, 9, 3]

# Feature dimension at each stage. Default: [96, 192, 384, 768]
_C.NPZNET.DIMS = [96, 192, 384, 768]

# Stochastic depth rate. Default: 0.
_C.NPZNET.DROP_PATH_RATE = 0.

# Init scaling value for classifier weights and biases. Default: 1.
_C.NPZNET.HEAD_INIT_SCALE = 1.


# -------------------------------- Batch norm options -------------------------------- #
_C.BN = CfgNode()

# BN epsilon
_C.BN.EPS = 1e-5

# BN momentum (BN momentum in PyTorch = 1 - BN momentum in Caffe2)
_C.BN.MOM = 0.1

# Precise BN stats
_C.BN.USE_PRECISE_STATS = True
_C.BN.NUM_SAMPLES_PRECISE = 8192

# Initialize the gamma of the final BN of each block to zero
_C.BN.ZERO_INIT_FINAL_GAMMA = False

# Use a different weight decay for BN layers
_C.BN.USE_CUSTOM_WEIGHT_DECAY = False
_C.BN.CUSTOM_WEIGHT_DECAY = 0.0


# -------------------------------- Layer norm options -------------------------------- #
_C.LN = CfgNode()

# LN epsilon
_C.LN.EPS = 1e-5

# Use a different weight decay for LN layers
_C.LN.USE_CUSTOM_WEIGHT_DECAY = False
_C.LN.CUSTOM_WEIGHT_DECAY = 0.0


# -------------------------------- Optimizer options --------------------------------- #
_C.OPTIM = CfgNode()

# Type of optimizer select from {'sgd', 'adam', 'adamw'}
_C.OPTIM.OPTIMIZER = "sgd"

# Learning rate ranges from BASE_LR to MIN_LR*BASE_LR according to the LR_POLICY
_C.OPTIM.BASE_LR = 0.1
_C.OPTIM.MIN_LR = 0.0

# Learning rate policy select from {'cos', 'exp', 'lin', 'steps'}
_C.OPTIM.LR_POLICY = "cos"

# Steps for 'steps' policy (in epochs)
_C.OPTIM.STEPS = []

# Learning rate multiplier for 'steps' policy
_C.OPTIM.LR_MULT = 0.1

# Maximal number of epochs
_C.OPTIM.MAX_EPOCH = 200

# Momentum
_C.OPTIM.MOMENTUM = 0.9

# Momentum dampening
_C.OPTIM.DAMPENING = 0.0

# Nesterov momentum
_C.OPTIM.NESTEROV = True

# Betas (for Adam/AdamW optimizer)
_C.OPTIM.BETA1 = 0.9
_C.OPTIM.BETA2 = 0.999

# L2 regularization
_C.OPTIM.WEIGHT_DECAY = 5e-4

# Use a different weight decay for all biases (excluding those in BN/LN layers)
_C.OPTIM.BIAS_USE_CUSTOM_WEIGHT_DECAY = False
_C.OPTIM.BIAS_CUSTOM_WEIGHT_DECAY = 0.0

# Start the warm up from OPTIM.BASE_LR * OPTIM.WARMUP_FACTOR
_C.OPTIM.WARMUP_FACTOR = 0.1

# Gradually warm up the OPTIM.BASE_LR over this number of epochs
_C.OPTIM.WARMUP_EPOCHS = 0

# Exponential Moving Average (EMA) update value
_C.OPTIM.EMA_ALPHA = 1e-5

# Iteration frequency with which to update EMA weights
_C.OPTIM.EMA_UPDATE_PERIOD = 32

# Enable usage of multi tensor apply optimizers for better performance.
_C.OPTIM.MTA = False


# --------------------------------- Training options --------------------------------- #
_C.TRAIN = CfgNode()

# Dataset and split
_C.TRAIN.DATASET = ""
_C.TRAIN.DATA_PATH = ""
_C.TRAIN.SPLIT = "train.json"
_C.TRAIN.PREPROCESS = "preprocess.pkl"

# Total mini-batch size
_C.TRAIN.BATCH_SIZE = 128

# Image size
_C.TRAIN.IM_SIZE = [224, 224]

# Resume training from the latest checkpoint in the output directory
_C.TRAIN.AUTO_RESUME = True

# Weights to start training from
_C.TRAIN.WEIGHTS = ""

# If True train using mixed precision
_C.TRAIN.MIXED_PRECISION = False

# Label smoothing value in 0 to 1 where (0 gives no smoothing)
_C.TRAIN.LABEL_SMOOTHING = 0.0


# --------------------------------- Testing options ---------------------------------- #
_C.TEST = CfgNode()

# Dataset and split
_C.TEST.DATASET = ""
_C.TEST.DATA_PATH = ""
_C.TEST.SPLIT = "test.json"

# Total mini-batch size
_C.TEST.BATCH_SIZE = 200

# Image size
_C.TEST.IM_SIZE = [256, 256]

# Weights to use for testing
_C.TEST.WEIGHTS = ""


# ------------------------------- Data loader options -------------------------------- #
_C.DATA_LOADER = CfgNode()

# Number of data loader workers per process
_C.DATA_LOADER.NUM_WORKERS = 8

# Load data to pinned host memory
_C.DATA_LOADER.PIN_MEMORY = True

# Data Loader mode to use ("pytorch", "ffcv")
_C.DATA_LOADER.MODE = "pytorch"


# ---------------------------------- CUDNN options ----------------------------------- #
_C.CUDNN = CfgNode()

# Perform benchmarking to select fastest CUDNN algorithms (best for fixed input sizes)
_C.CUDNN.BENCHMARK = True


# ------------------------------- Precise time options ------------------------------- #
_C.PREC_TIME = CfgNode()

# Number of iterations to warm up the caches
_C.PREC_TIME.WARMUP_ITER = 3

# Number of iterations to compute avg time
_C.PREC_TIME.NUM_ITER = 30


# --------------------------------- FSDP keys -----------------------------------------#
_C.FSDP = CfgNode()

# Enable FSDP sharding
_C.FSDP.ENABLED = False

# Enable resharding after the FW pass. This saves memory but tradesoff communication.
_C.FSDP.RESHARD_AFTER_FW = True

# Enable wrapping LayerNorm in a FSDP wrapper which allows weights and stats to remain in FP32.
_C.FSDP.LAYER_NORM_FP32 = True


# ----------------------------------- Misc options ----------------------------------- #
# Optional description of a config
_C.DESC = ""

# If True output additional info to log
_C.VERBOSE = True

# Number of GPUs to use (applies to both training and testing)
_C.NUM_GPUS = 1

# Maximum number of GPUs available per node (unlikely to need to be changed)
_C.MAX_GPUS_PER_NODE = 8

# Output directory
_C.OUT_DIR = "/workspace/runs"

# Config destination (in OUT_DIR)
_C.CFG_DEST = "config.yaml"

# Note that non-determinism is still be present due to non-deterministic GPU ops
_C.RNG_SEED = 1

# Log destination ('stdout' or 'file')
_C.LOG_DEST = "stdout"

# Log period in iters
_C.LOG_PERIOD = 10

# Distributed backend
_C.DIST_BACKEND = "nccl"

# Hostname and port range for multi-process groups (actual port selected randomly)
_C.HOST = "localhost"
_C.PORT_RANGE = [10000, 65000]

# Models weights referred to by URL are downloaded to this local cache
_C.DOWNLOAD_CACHE = "/workspace/runs/quant-download-cache"


# ---------------------------------- Default config ---------------------------------- #
_CFG_DEFAULT = _C.clone()
_CFG_DEFAULT.freeze()


def assert_cfg():
    """Checks config values invariants."""
    err_str = "The first lr step must start at 0"
    assert not _C.OPTIM.STEPS or _C.OPTIM.STEPS[0] == 0, err_str
    err_str = "Mini-batch size should be a multiple of NUM_GPUS."
    assert _C.TRAIN.BATCH_SIZE % _C.NUM_GPUS == 0, err_str
    assert _C.TEST.BATCH_SIZE % _C.NUM_GPUS == 0, err_str
    err_str = "Log destination '{}' not supported"
    assert _C.LOG_DEST in ["stdout", "file"], err_str.format(_C.LOG_DEST)
    err_str = "NUM_GPUS must be divisible by or less than MAX_GPUS_PER_NODE"
    num_gpus, max_gpus_per_node = _C.NUM_GPUS, _C.MAX_GPUS_PER_NODE
    assert num_gpus <= max_gpus_per_node or num_gpus % max_gpus_per_node == 0, err_str


def dump_cfg():
    """Dumps the config to the output directory."""
    cfg_file = os.path.join(_C.OUT_DIR, _C.CFG_DEST)
    with pathmgr.open(cfg_file, "w") as f:
        _C.dump(stream=f)
    return cfg_file


def load_cfg(cfg_file):
    """Loads config from specified file."""
    with pathmgr.open(cfg_file, "r") as f:
        _C.merge_from_other_cfg(_C.load_cfg(f))


def reset_cfg():
    """Reset config to initial state."""
    _C.merge_from_other_cfg(_CFG_DEFAULT)
