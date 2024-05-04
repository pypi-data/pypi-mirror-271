# imgcv

Image Processing Library from scratch using Python.

[![Documentation Status](https://readthedocs.org/projects/imgcv/badge/?version=latest)](https://imgcv.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/imgcv)](https://pypi.org/project/imgcv/)
![GitHub Workflow Status](https://github.com/Preet-Sojitra/imgcv/actions/workflows/ci-cd.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> NOTE: This library is just a fun project to learn about image processing and computer vision algorithms from scratch and to enhance my understanding of the concepts. 

---
Various implemenatations of image processing algorithms from scratch using Python has been implemented in [this repository](https://github.com/Preet-Sojitra/DIP) as part of Digital Image Processing course at my university.


## Installation

```bash
$ pip install imgcv
```

## Usage

```python
from PIL import Image
from imgcv.transformation.negative import negative_transform

# Load image
img = Image.open('path/to/image.jpg')

# Convert image to numpy array
img = np.array(img)

# Apply logarithmic transformation
img = negative_transform(img)

# Convert numpy array to image
img = Image.fromarray(img)

# show image
img.show()
```

## Documentation

The official documentation is hosted on Read the Docs: [imgcv Documentation](https://imgcv.readthedocs.io/en/latest/index.html)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`imgcv` was created by Preet Sojitra. It is licensed under the terms of the MIT license.

## Credits

`imgcv` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
