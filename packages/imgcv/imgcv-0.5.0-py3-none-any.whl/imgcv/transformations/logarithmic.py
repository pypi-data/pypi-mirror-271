import numpy as np
from imgcv.common import check_image


def logarithmic_transform(image, c=1):
    """Apply logarithmic transformation to the input image

    Formula:
        s = c * log(1 + r)

    Args:
        image (ndarray): Input image to be transformed
        c (float): Constant value to scale the logarithmic transformation

    Raises:
        TypeError: If the input is not a numpy array
        ValueError: If the input is not a grayscale or color image

    Returns:
        np.ndarray: Transformed image
    """

    check_image(image)

    # Normalizing the image
    image = image / 255.0

    # Applying the logarithmic transformation
    transformed_img = c * np.log(1 + image)
    transformed_img = (transformed_img * 255.0).astype(np.uint8)

    return transformed_img
