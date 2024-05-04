import numpy as np
from imgcv.common import check_image


def reduce_gray_levels(image, k):
    """Reduce the number of gray levels in the input image to desired levels

    Args:
        image (np.ndarray): Input image to be transformed
        k (int): Desired number of bits to represent the image. The number of intensity levels will be 2^k. For example, if k=2, the number of intensity levels will be 4.

    Raises:
        TypeError: If the input is not a numpy array
        ValueError: If the input is not a grayscale or color image

    Returns:
        np.ndarray: Image with reduced gray levels
    """

    check_image(image)

    if len(image.shape) == 2:
        intensity_levels = 2**k
        compression_ratio = 256 / intensity_levels
        reduced_image = np.floor(image / compression_ratio) * compression_ratio
        return reduced_image
    else:
        # need to tackle each channel separately
        reduced_image = np.zeros_like(image)
        for i in range(image.shape[2]):
            reduced_image[:, :, i] = reduce_gray_levels(image[:, :, i], k)

        return reduced_image
