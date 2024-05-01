## Installation:

`pip install torch_image2vector`

Install from github:  
`pip install git+https://github.com/MajewskiLukasz/torch_image2vector.git`


## List of available models

### ResNet Models
| Model      | Vector Length |
|------------|---------------|
| resnet-18  | 512           |
| resnet-34  | 512           |
| resnet-50  | 2048          |
| resnet-101 | 2048          |
| resnet-152 | 2048          |

### ResNeXt Models
| Model              | Vector Length |
|--------------------|---------------|
| resnext50_32x4d    | 2048          |
| resnext101_32x8d   | 2048          |
| resnext101_32x8d_wsl | 2048        |

### EfficientNet Models
| Model             | Vector Length |
|-------------------|---------------|
| efficientnet_b0   | 1280          |
| efficientnet_b1   | 1280          |
| efficientnet_b2   | 1408          |
| efficientnet_b3   | 1536          |
| efficientnet_b4   | 1792          |
| efficientnet_b5   | 2048          |
| efficientnet_b6   | 2304          |
| efficientnet_b7   | 2560          |

### MobileNet Models
| Model             | Vector Length |
|-------------------|---------------|
| mobilenet_v3_large | 960          |

### ConvNext Models
| Model             | Vector Length |
|-------------------|---------------|
| convnext_tiny     | 768           |
| convnext_small    | 768           |
| convnext_base     | 1024          |
| convnext_large    | 1536          |

**Note**: If you are looking for a specific model not listed above, you can check the [PyTorch Hub](https://pytorch.org/hub/) for more pre-trained models.

## Recommended setup

in case of light embeddings extraction with good performance for similarity-search, its recommended to use
`model=mobilenet_v3_large` with `weights_version=mobilenet_v3_large-8738ca79`
for results consistancy with other projects Refer to **requirements.txt** for
recommended versions of `torch` and `torchvision` these are not must but loading
specifc `weights_version` requires matching specific `torch` and `torchvision`
versions (or higher)

## Test

`bash run_test.sh`

## Use

### 1. Inference on loaded images

```python
from PIL import Image
from torch_image2vector import Image2Vector


# Initialize Image2Vector
image2vector = Image2Vector(model="resnet50")

# Read in an image (rgb format)
img = Image.open('sample.jpg')
# Get a vector from image2vector
vec = image2vector.get_vec(img)
# [Alternative - batch processing] submit a list of images
vectors = image2vector.get_vec([img, img2, img3])
```

### 2. Inference on large number of images

For a large number of images, to improve inference speed, it is recommended to
use the following pipeline:

```python
import torch
from torch.utils.data import Dataset, DataLoader
from torch_image2vector import Image2Vector, ModelInference
from torch_image2vector.data import ImgPathsDataset

# Select batch size relative to your GPU capacity
batch_size = 128
num_workers = 8
# List of image files we want to run inference on.
image_files = ['sample.png', ...]

# Initialize Image2Vector with CUDA for speed.
image2vector = Image2Vector(cuda=True, model="mobilenet_v3_large", weights_version="mobilenet_v3_large-8738ca79")
# Create dataset from image paths and corresponding loader.
dataset = ImgPathsDataset(image_files, image2vector.transform)
loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
vec_list = []
for data in loader:
    vec_list.append(image2vector._loader_forward(data.to(image2vector.device)))
# (N, dim) array of embeddings.
vec = np.vstack(vec_list)
```
