import numpy as np


def check_image(image):
    """Check if the input is a numpy array

    Args:
        image (np.ndarray): Input image to be transformed

    Raises:
        TypeError: If the input is not a numpy array
        ValueError: If the input is not a grayscale or color image
    """
    if not isinstance(image, np.ndarray):
        raise TypeError(
            f"Input should be a numpy array. Expected <class 'numpy.ndarray'>, but got {type(image)}"
        )

    if len(image.shape) not in [2, 3]:
        raise ValueError(
            f"Input should be grayscale or color image. Got {len(image.shape)} dimensions"
        )
