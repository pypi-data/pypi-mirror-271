import pathlib

import numpy as np
from quant.football.transforms import get_table_factory
from quant.utils.io import auto_load, auto_save, copy_file


def make_splits(data_path, labels_file):
    data_path = pathlib.Path(data_path)

    labels = auto_load(data_path / labels_file)

    groups = sorted(set([d["group"] for d in labels.values()]))
    splits = {group: [] for group in groups}

    for d in labels.values():
        splits[d["group"]].append((d["name"], d["class"]))

    logs = []
    for group, data in splits.items():
        auto_save(data_path / f"{group}.json", data)
        logs.append(f"{group} data: {len(data)}")
    return ", ".join(logs)


def compute_scale_params(data_path, preprocess_file, labels_file):
    data_path = pathlib.Path(data_path)

    labels = auto_load(data_path / labels_file)

    preprocess_params = auto_load(data_path / preprocess_file)

    table_factory = get_table_factory(preprocess_params["table_name"])

    channel_sum, channel_sq_sum, total_pixels = 0, 0, 0
    for file in sorted(data_path.glob("*.npz")):
        if file.stem not in labels:
            continue

        data = auto_load(file)

        kwargs = preprocess_params

        time_range = kwargs["time_range"]
        time_low = time_range[0] + 0.1
        time_high = min(time_range[1], data["atime"].max())
        for curr_time in np.random.uniform(time_low, time_high, 5):
            img = table_factory.get_sample(curr_time, **data, **kwargs)

            channel_sum += np.sum(img, axis=(0, 1))
            channel_sq_sum += np.sum(img ** 2, axis=(0, 1))
            total_pixels += img.shape[0] * img.shape[1]

    eps = 1e-6
    mean = channel_sum / total_pixels
    std = np.sqrt(channel_sq_sum / total_pixels - mean ** 2)

    preprocess_params["scale_x_add"] = 0.0 - mean.astype(np.float32)
    preprocess_params["scale_x_mul"] = 1.0 / (std + eps).astype(np.float32)

    copy_file(data_path / preprocess_file, data_path / (preprocess_file + ".old"))
    auto_save(data_path / preprocess_file, preprocess_params)

    return preprocess_params
