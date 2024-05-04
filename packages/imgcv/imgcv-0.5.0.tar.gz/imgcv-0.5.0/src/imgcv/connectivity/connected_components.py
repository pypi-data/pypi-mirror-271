from imgcv.common import check_image
import numpy as np


def connected_component_analysis(im):
    """Peforms connected component analysis on a binary image. Currently only 4-connected component analysis is supported.

    NOTE: The input image should be a binary image. Non-zero pixels are considered as foreground. This function will not work properly if the input image is not binary.

    Args:
        im (np.ndarray): Binary image. Non-zero pixels are considered as foreground

    Raises:
        ValueError: If the input image is not binary

    Returns:
        np.ndarray: Image with connected components labeled. Each connected component will have a unique label
        int: Number of connected components in the image
    """

    # check if the input image is valid
    check_image(im)

    # check if the image is binary
    if not _is_binary(im):
        raise ValueError("The input image is not binary")

    connected_components = np.zeros_like(im, dtype=np.uint8)

    window = np.zeros((2, 2), dtype=np.uint8)

    # padding the image
    padded_im = np.pad(im, 1, mode="constant")

    label_counter = 1
    equivalence = {}

    # first pass
    for row in range(padded_im.shape[0] - 1):
        for col in range(padded_im.shape[1] - 1):
            window = padded_im[row : row + 2, col : col + 2]
            main_pixel = window[
                1, 1
            ]  # bottom right corner will be our main pixel as our image is padded

            # We are only interested in those pixels whose intensity is 1. So, if the main pixel is 0, then we will skip
            if main_pixel == 0:
                continue

            # if both left and top pixels are 0, then assign a new label
            if window[0, 1] == 0 and window[1, 0] == 0:
                connected_components[row, col] = label_counter
                equivalence[label_counter] = label_counter
                label_counter += 1

            # if both are not 0, then assign the minimum label and update the equivalence dictionary
            elif window[1, 0] != 0 and window[0, 1] != 0:
                connected_components[row, col] = min(
                    connected_components[row - 1, col],
                    connected_components[row, col - 1],
                )
                equivalence[
                    max(
                        connected_components[row - 1, col],
                        connected_components[row, col - 1],
                    )
                ] = min(
                    connected_components[row - 1, col],
                    connected_components[row, col - 1],
                )

            # if any one of the pixel is 0, then assign the non-zero label
            else:
                connected_components[row, col] = max(
                    connected_components[row - 1, col],
                    connected_components[row, col - 1],
                )
                equivalence[
                    max(
                        connected_components[row - 1, col],
                        connected_components[row, col - 1],
                    )
                ] = max(
                    connected_components[row - 1, col],
                    connected_components[row, col - 1],
                )

    # second pass
    # replace the labels with the equivalent labels
    for key, value in equivalence.items():
        connected_components[connected_components == key] = value

    # Number of connected components
    no_of_connected_components = len(np.unique(connected_components)) - 1

    """
    connected_components includes the labels of the connected components. The user can now use this in any way they want. For example, they can find the number of connected components, the area of each connected component, etc. They can even extract the connected components from the original image using these labels.
    """
    return connected_components, no_of_connected_components


def _is_binary(im):
    """Checks if the image is binary or not. A binary image is an image that has only two pixel values. For example, 0 and 1.

    Returns:
        Boolean: True if the image is binary, False otherwise
    """

    pixels = np.unique(im)
    return np.array_equal(pixels, np.array([0, 1]))
