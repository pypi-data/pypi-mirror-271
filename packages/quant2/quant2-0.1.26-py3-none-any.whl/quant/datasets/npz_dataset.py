import numpy as np
import pathlib
import quant.core.logging as logging
import torch.utils.data
from quant.core.config import cfg
from quant.core.io import pathmgr
from quant.football.transforms import get_table_factory
from quant.utils.io import load_json, load_npz, load_pkl


logger = logging.get_logger(__name__)


def channel_norm(x, x_add, x_mul):
    return (x + x_add) * x_mul


class NpzDataset(torch.utils.data.Dataset):
    """NpzDataset dataset."""

    def __init__(self, data_path, split):
        assert pathmgr.exists(data_path), "Data path '{}' not found".format(data_path)
        self._data_path, self._split = pathlib.Path(data_path), split
        logger.info("Constructing NpzDataset {}...".format(split))
        self._construct_dataset()

    def _construct_dataset(self):
        _data_path, _split = self._data_path, self._split
        logger.info("{} data path: {}".format(_split, _data_path))
        self.preprocess_kwargs = load_pkl(_data_path / cfg.TRAIN.PREPROCESS)
        self.table_factory = get_table_factory(self.preprocess_kwargs["table_name"])
        self._imdb = []
        for im_name, cls_id in load_json(_data_path / _split):
            self._imdb.append({"im_path": str(_data_path / im_name), "class": cls_id})
        logger.info("Number of images: {}".format(len(self._imdb)))

    def _prepare_im(self, im_path):
        """Prepares the image for network input."""
        data = load_npz(im_path)

        kwargs = self.preprocess_kwargs

        time_range = kwargs["time_range"]
        time_low = time_range[0] + 0.1
        time_high = min(time_range[1], data["atime"].max())
        curr_time = np.random.uniform(time_low, time_high, None)

        im = self.table_factory.get_sample(curr_time, **data, **kwargs)
        # For training and testing use channel normalization
        im = channel_norm(im, kwargs["scale_x_add"], kwargs["scale_x_mul"])
        # Convert HWC/float to CHW/float format
        im = np.ascontiguousarray(im.transpose([2, 0, 1]))
        return im.astype(np.float32)

    def __getitem__(self, index):
        # Load the image
        im_path = self._imdb[index]["im_path"]
        # Prepare the image for training / testing
        im = self._prepare_im(im_path)
        # Retrieve the label
        label = self._imdb[index]["class"]
        return im, label

    def __len__(self):
        return len(self._imdb)
