import torch
from quant.core.config import cfg
from quant.datasets.npz_dataset import NpzDataset
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler


# Supported datasets
_DATASETS = {
    "npzdataset": NpzDataset,
}


def _construct_loader(dataset_name, data_path, split, batch_size, shuffle, drop_last):
    """Constructs the data loader for the given dataset."""
    err_str = "Dataset '{}' not supported".format(dataset_name)
    assert dataset_name in _DATASETS, err_str
    # Construct the dataset
    dataset = _DATASETS[dataset_name](data_path, split)
    # Create a sampler for multi-process training
    sampler = DistributedSampler(dataset) if cfg.NUM_GPUS > 1 else None
    # Create a loader
    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=(False if sampler else shuffle),
        sampler=sampler,
        num_workers=cfg.DATA_LOADER.NUM_WORKERS,
        pin_memory=cfg.DATA_LOADER.PIN_MEMORY,
        drop_last=drop_last,
    )
    return loader


def _construct_loader_ffcv(dataset_name, data_path, split, batch_size, shuffle, drop_last):
    raise NotImplementedError


def construct_train_loader():
    """Train loader wrapper."""
    if cfg.DATA_LOADER.MODE == "ffcv":
        return _construct_loader_ffcv(
            dataset_name=cfg.TRAIN.DATASET,
            data_path=cfg.TRAIN.DATA_PATH,
            split=cfg.TRAIN.SPLIT,
            batch_size=int(cfg.TRAIN.BATCH_SIZE / cfg.NUM_GPUS),
            shuffle=True,
            drop_last=True,
        )
    return _construct_loader(
        dataset_name=cfg.TRAIN.DATASET,
        data_path=cfg.TRAIN.DATA_PATH,
        split=cfg.TRAIN.SPLIT,
        batch_size=int(cfg.TRAIN.BATCH_SIZE / cfg.NUM_GPUS),
        shuffle=True,
        drop_last=True,
    )


def construct_test_loader():
    """Test loader wrapper."""
    if cfg.DATA_LOADER.MODE == "ffcv":
        return _construct_loader_ffcv(
            dataset_name=cfg.TEST.DATASET,
            data_path=cfg.TEST.DATA_PATH,
            split=cfg.TEST.SPLIT,
            batch_size=int(cfg.TEST.BATCH_SIZE / cfg.NUM_GPUS),
            shuffle=False,
            drop_last=False,
        )
    return _construct_loader(
        dataset_name=cfg.TEST.DATASET,
        data_path=cfg.TEST.DATA_PATH,
        split=cfg.TEST.SPLIT,
        batch_size=int(cfg.TEST.BATCH_SIZE / cfg.NUM_GPUS),
        shuffle=False,
        drop_last=False,
    )


def shuffle(loader, cur_epoch):
    """Shuffles the data."""
    err_str = "Sampler type '{}' not supported".format(type(loader.sampler))
    assert isinstance(loader.sampler, (RandomSampler, DistributedSampler)), err_str
    # RandomSampler handles shuffling automatically
    if isinstance(loader.sampler, DistributedSampler):
        # DistributedSampler shuffles data based on epoch
        loader.sampler.set_epoch(cur_epoch)
