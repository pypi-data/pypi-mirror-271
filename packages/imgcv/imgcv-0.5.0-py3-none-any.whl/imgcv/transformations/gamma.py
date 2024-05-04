import numpy as np
from imgcv.common import check_image


def gamma_correction(image, gamma=1.0, c=1):
    """Applies gamma correction to the image.

    Formula:
        gamma_correction = c * (image ** gamma)

    Args:
        image (np.ndarray): Image to be transformed.
        gamma (float, optional): Power value . Defaults to 1.0.
        c (int, optional): Constant value. Defaults to 1.

    Returns:
        np.ndarray: Transformed image.
    """

    check_image(image)

    norm_img = image / 255.0
    corrected_img = c * (norm_img**gamma)

    # Clip the values to be in the range [0, 1] since gamma correction can result in overflow
    corrected_img = np.clip(corrected_img, 0, 1)
    # scale the values back to [0, 255]
    corrected_img = (corrected_img * 255).astype(np.uint8)

    return corrected_img
