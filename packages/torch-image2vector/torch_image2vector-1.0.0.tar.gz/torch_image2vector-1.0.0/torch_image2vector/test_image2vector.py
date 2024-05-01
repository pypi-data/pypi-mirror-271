import os
import pathlib
import unittest

import numpy as np
import torch
from PIL import Image, ImageDraw
from torch.utils.data import DataLoader

from . import Image2Vector, ImgPathsDataset


def imageGen():
    """Generate image for test."""
    img = Image.new(mode="RGB", size=(1000, 500), color=(200, 120, 190))
    draw = ImageDraw.Draw(img)
    draw.polygon([(200, 10), (200, 200), (150, 50)], fill="yellow")
    return img


class TestExtractor(unittest.TestCase):
    def test_resnet18(self):
        img = imageGen()
        image2vector = Image2Vector(model="resnet18", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_resnet50(self):
        img = imageGen()
        image2vector = Image2Vector(model="resnet50", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_resnext50_32x4d(self):
        img = imageGen()
        image2vector = Image2Vector(model="resnext50_32x4d", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_resnext101_32x8d_wsl(self):
        img = imageGen()
        image2vector = Image2Vector(model="resnext101_32x8d_wsl", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_efficientnet_b0(self):
        img = imageGen()
        image2vector = Image2Vector(model="efficientnet_b0", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_mobilenet_v3(self):
        img = imageGen()
        image2vector = Image2Vector(model="mobilenet_v3_large", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_mobilenet_v3_single_array_element(self):
        img = imageGen()
        image2vector = Image2Vector(model="mobilenet_v3_large", progress=False)
        res = image2vector.get_vec([img])
        self.assertEqual(1, len(res))
        vec = res[0]
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_mobilenet_v3_single_array_element_gpu(self):
        img = imageGen()
        image2vector = Image2Vector(cuda=torch.cuda.is_available(), model="mobilenet_v3_large", progress=False)
        res = image2vector.get_vec([img])
        self.assertEqual(1, len(res))
        vec = res[0]
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_convnext_tiny(self):
        img = imageGen()
        image2vector = Image2Vector(model="convnext_tiny", progress=False)
        vec = image2vector.get_vec(img)
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual("float32", vec.dtype)
        self.assertEqual(1, vec.ndim)
        self.assertEqual(image2vector.layer_output_size, vec.size)

    def test_tensor_output(self):
        img = imageGen()
        image2vector = Image2Vector(model="mobilenet_v3_large", progress=False)
        vec = image2vector.get_vec(img, tensor=True)
        self.assertEqual(True, torch.is_tensor(vec))
        self.assertEqual(image2vector.layer_output_size, vec.size()[0])
        self.assertEqual(image2vector.layer_output_size, len(torch.flatten(vec)))

    def test_basic_batch_inference(self):
        img = imageGen()
        image2vector = Image2Vector(model="mobilenet_v3_large", progress=False)
        vec = image2vector.get_vec([img, img])
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual((2, image2vector.layer_output_size), vec.shape)

    def test_basic_batch_inference_gpu(self):
        img = imageGen()
        image2vector = Image2Vector(cuda=torch.cuda.is_available(), model="mobilenet_v3_large", progress=False)
        vec = image2vector.get_vec([img, img])
        self.assertEqual(True, isinstance(vec, np.ndarray))
        self.assertEqual((2, image2vector.layer_output_size), vec.shape)

    def test_loader_batch_inference_cpu(self):
        img = imageGen()
        # Save image as path for loader
        img.save("generated.png")
        batch_size = 5
        num_workers = 1
        image_files = batch_size * ["generated.png"]
        image2vector = Image2Vector(cuda=False, model="mobilenet_v3_large", progress=False)
        dataset = ImgPathsDataset(image_files, image2vector.transform)
        loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        )
        vec_list = []
        for data in loader:
            vec_list.append(image2vector._loader_forward(data.to(image2vector.device)))
        vec = np.vstack(vec_list)
        self.assertEqual((batch_size, image2vector.layer_output_size), vec.shape)
        self.assertEqual(True, isinstance(vec, np.ndarray))

    def test_loader_batch_inference_gpu(self):
        img = imageGen()
        # Save image as path for loader
        img.save("generated.png")
        batch_size = 5
        num_workers = 1
        image_files = batch_size * ["generated.png"]
        image2vector = Image2Vector(cuda=torch.cuda.is_available(), model="mobilenet_v3_large", progress=False)
        dataset = ImgPathsDataset(image_files, image2vector.transform)
        loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        )
        vec_list = []
        for data in loader:
            vec_list.append(image2vector._loader_forward(data.to(image2vector.device)))
        vec = np.vstack(vec_list)
        self.assertEqual((batch_size, image2vector.layer_output_size), vec.shape)
        self.assertEqual(True, isinstance(vec, np.ndarray))

    def test_model_download(self):
        img = imageGen()
        image2vector = Image2Vector(
            model="mobilenet_v3_large", weights_version="mobilenet_v3_large-8738ca79", progress=False
        )
        vec = image2vector.get_vec(img, tensor=True)
        # road reference vector
        content = np.loadtxt("./torch_image2vector/reference_vector.txt")

        self.assertEqual(True, torch.is_tensor(vec))
        self.assertEqual(image2vector.layer_output_size, vec.size()[0])
        self.assertEqual(image2vector.layer_output_size, len(torch.flatten(vec)))
        self.assertEqual(True, (np.allclose(vec, content, rtol=1e-03, atol=1e-05)))

    def test_model_local(self):
        img = imageGen()
        weights_version = "mobilenet_v3_large-8738ca79.pth"
        cache_dir = f"{os.path.expanduser('~')}/.cache/torch/hub/checkpoints/"
        pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)
        # remove wieghts from cache
        if os.path.isfile(f"{cache_dir}{weights_version}"):
            os.remove(f"{cache_dir}{weights_version}")
        # get specified model weights
        torch.hub.download_url_to_file(
            f"https://download.pytorch.org/models/{weights_version}", f"{cache_dir}{weights_version}"
        )

        image2vector = Image2Vector(model="mobilenet_v3_large", model_path=f"{cache_dir}{weights_version}")
        vec = image2vector.get_vec(img, tensor=True)
        # road reference vector
        content = np.loadtxt("./torch_image2vector/reference_vector.txt")

        self.assertEqual(True, torch.is_tensor(vec))
        self.assertEqual(image2vector.layer_output_size, vec.size()[0])
        self.assertEqual(image2vector.layer_output_size, len(torch.flatten(vec)))
        self.assertEqual(True, (np.allclose(vec, content, rtol=1e-03, atol=1e-05)))


if __name__ == "__main__":
    unittest.main()
