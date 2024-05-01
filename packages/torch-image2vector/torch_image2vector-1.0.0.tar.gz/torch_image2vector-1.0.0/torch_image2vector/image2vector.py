import os
from typing import Optional

import numpy as np
import torch
import torchvision


class Image2Vector:
    # Base model configs come from torchvision.models
    MODELS_CONFIG = {
        "resnet18": {"size": 512, "weights": "IMAGENET1K_V1"},
        "resnet34": {"size": 512, "weights": "IMAGENET1K_V1"},
        "resnet50": {"size": 2048, "weights": "IMAGENET1K_V2"},
        "resnet101": {"size": 2048, "weights": "IMAGENET1K_V2"},
        "resnet152": {"size": 2048, "weights": "IMAGENET1K_V2"},
        "resnext50_32x4d": {"size": 2048, "weights": "IMAGENET1K_V2"},
        "resnext101_32x8d": {"size": 2048, "weights": "IMAGENET1K_V2"},
        "efficientnet_b0": {"size": 1280, "weights": "IMAGENET1K_V1"},
        "efficientnet_b2": {"size": 1408, "weights": "IMAGENET1K_V1"},
        "efficientnet_b3": {"size": 1536, "weights": "IMAGENET1K_V1"},
        "efficientnet_b4": {"size": 1792, "weights": "IMAGENET1K_V1"},
        "efficientnet_b5": {"size": 2048, "weights": "IMAGENET1K_V1"},
        "efficientnet_b6": {"size": 2304, "weights": "IMAGENET1K_V1"},
        "efficientnet_b7": {"size": 2560, "weights": "IMAGENET1K_V1"},
        "mobilenet_v3_large": {"size": 960, "weights": "IMAGENET1K_V2"},
        "convnext_tiny": {"size": 768, "weights": "IMAGENET1K_V1"},
        "convnext_small": {"size": 768, "weights": "IMAGENET1K_V1"},
        "convnext_base": {"size": 1024, "weights": "IMAGENET1K_V1"},
        "convnext_large": {"size": 1536, "weights": "IMAGENET1K_V1"},
    }
    # Facebook hub
    FB_MODELS_CONFIG = {
        "resnext101_32x8d_wsl": {"size": 2048, "weights": "IMAGENET1K_V2"},
    }

    def __init__(
        self,
        cuda: bool = False,
        model: str = "mobilenet_v3_large",
        layer: str = "default",
        layer_output_size: int = 960,
        gpu_no: int = 0,
        model_path: Optional[str] = None,
        weights_version: Optional[str] = None,
        progress: bool = True,
    ):
        """Image2Vector
        :param cuda: If set to True, will run forward pass on GPU
        :param model: String name of requested model
        :param layer: String or Int depending on model.
        :param layer_output_size: Int output size of the requested layer
        :param gpu_no: Selection of gpu.
        :param model_path: Model local path.
        :param weights_version: Specific weights version.
        :param progress: If True, displays a progress bar of the download to stderr. Default is True.
        """
        self.device = torch.device(f"cuda:{gpu_no}" if cuda else "cpu")
        assert any(
            [model in group for group in [self.FB_MODELS_CONFIG, self.MODELS_CONFIG]]
        ), f"Model {model} not supported."
        self.model_name = model
        self.layer = layer
        self.layer_output_size = layer_output_size
        self.model_path = model_path
        self.weights_version = weights_version
        self.progress = progress

        # Find which HUB the model is in
        if self.model_name in self.FB_MODELS_CONFIG:
            self.model_config = self.FB_MODELS_CONFIG[self.model_name]
            # walkaround with infinite lool in _validate_not_a_forked_repo
            torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
            self.model = torch.hub.load("facebookresearch/WSL-Images", self.model_name, progress=self.progress)
        else:
            self.model_config = self.MODELS_CONFIG[self.model_name]
            if self.model_path or self.weights_version is not None:
                self.model = eval(f"torchvision.models.{self.model_name}()")
                self.model = self._load_model_version(self.model)
            else:
                self.model = eval(
                    f"torchvision.models.{self.model_name}('{self.model_config['weights']}', progress={self.progress})"
                )

        if self.layer == "default":
            self.extraction_layer = self.model._modules.get("avgpool")
            assert isinstance(self.model_config["size"], int)
            self.layer_output_size = self.model_config["size"]
        else:
            self.extraction_layer = self.model._modules.get(self.layer_output_size)

        self.model = self.model.to(self.device)

        self.model.eval()

        self.transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.Resize(226),
                torchvision.transforms.CenterCrop((224, 224)),
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

    def _load_model_version(self, model: torch.nn.Module) -> torch.nn.Module:
        """Loading specific weights from local or download to cache and load
        :param model: torch model to load weights
        :param weights_version: pass version of weights maching model (IMAGENET1K_V1 or IMAGENET1K_V2)
        :returns: torch model with loaded weights
        """
        if self.model_path is not None:
            model.load_state_dict(torch.load(self.model_path))
            return model
        elif self.weights_version is not None:
            # check if model already exists in cache
            cache_model = f"{os.path.expanduser('~')}/.cache/torch/hub/checkpoints/{self.weights_version}.pth"
            if not os.path.isfile(cache_model):
                # assure that path already exists
                if not os.path.exists(f"{os.path.expanduser('~')}/.cache/torch/hub/checkpoints/"):
                    os.makedirs(f"{os.path.expanduser('~')}/.cache/torch/hub/checkpoints/")
                # download specific weightes to cache
                torch.hub.download_url_to_file(
                    f"https://download.pytorch.org/models/{self.weights_version}.pth",
                    cache_model,
                    progress=self.progress,
                )
            model.load_state_dict(torch.load(cache_model))
            return model

    def get_vec(self, img, tensor=False):
        """Get vector embedding from PIL image
        :param img: PIL Image or list of PIL Images
        :param tensor: If True, get_vec will return a FloatTensor instead of Numpy array
        :returns: Numpy float32 ndarray
        """
        if isinstance(img, list):
            a = [self.transform(im) for im in img]
            images = torch.stack(a).to(self.device)
        else:
            images = self.transform(img).unsqueeze(0).to(self.device)

        if "efficientnet" in self.model_name:
            my_embedding = torch.zeros(images.size()[0], self.layer_output_size, 7, 7)
        else:
            my_embedding = torch.zeros(images.size()[0], self.layer_output_size, 1, 1)

        def copy_data(*o):
            my_embedding.copy_(o[-1].data)

        h = self.extraction_layer.register_forward_hook(copy_data)
        with torch.no_grad():
            self.model(images)
        h.remove()

        if tensor:
            my_embedding = my_embedding[:, :, 0, 0]
            return my_embedding if isinstance(img, list) else my_embedding.squeeze(0)
        else:
            if self.model_name == "efficientnet" in self.model_name:
                result = torch.mean(my_embedding, (2, 3), True).numpy()[:, :, 0, 0]
                return result if isinstance(img, list) else np.squeeze(result)

            result = my_embedding.numpy()[:, :, 0, 0]
            return result if isinstance(img, list) else np.squeeze(result)

    def _loader_forward(self, image_tensors: torch.tensor) -> torch.tensor:
        """Function for forward pass on already processed image_tensors.

        Args:
            image_tensors (torch.tensor): (N, C, H, W) batch of processed image tensors.
        """
        image_tensors.to(self.device)
        batch_size = image_tensors.shape[0]
        if "efficientnet" in self.model_name:
            my_embedding = torch.zeros(batch_size, self.layer_output_size, 7, 7)
        else:
            my_embedding = torch.zeros(batch_size, self.layer_output_size, 1, 1)

        def copy_data(*o):
            my_embedding.copy_(o[-1].data)

        h = self.extraction_layer.register_forward_hook(copy_data)
        with torch.no_grad():
            self.model(image_tensors)
        h.remove()

        result = my_embedding.numpy()[:, :, 0, 0]
        return result if result.shape[0] > 1 else np.squeeze(result)
