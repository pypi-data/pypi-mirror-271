from typing import Callable

import torch
from PIL import Image
from torch.utils.data import Dataset


class ImgPathsDataset(Dataset):
    """Image paths dataset."""

    def __init__(self, image_paths: list, transform: Callable):
        """
        Args:
            image_paths (list): List of image paths to run on.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        image = self.transform(Image.open(self.image_paths[idx]))
        return image
