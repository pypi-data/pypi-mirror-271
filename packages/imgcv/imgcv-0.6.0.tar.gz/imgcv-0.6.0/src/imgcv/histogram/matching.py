import numpy as np
from imgcv.common import check_image


def matchHistogram(image, reference):
    """Matches the histogram of the image to the reference image. Works for both grayscale and color images. Matching is done for each channel seperately.

    Args:
        image (np.ndarray): The input image
        reference (np.ndarray): The reference image

    Raises:
        ValueError: Thrown when the number of channels in the image and reference are not same

    Returns:
        ndarray: The matched image
        tuple: The source cumulative distribution function and the source histogram
        tuple: The reference cumulative distribution function and the reference histogram
    """

    check_image(image)
    check_image(reference)

    if image.ndim != reference.ndim:
        raise ValueError(
            f"Both the images should have same number of channels. Image has {image.ndim} channels and reference has {reference.ndim} channels"
        )

    if image.ndim == 3:

        source_cdf = {"R": None, "G": None, "B": None}
        source_hist = {"R": None, "G": None, "B": None}

        reference_cdf = {"R": None, "G": None, "B": None}

        reference_hist = {"R": None, "G": None, "B": None}

        matched = np.zeros_like(image)

        for channel in range(image.shape[-1]):
            matched_channel, source, template = _match_cumulative_cdf(
                image[..., channel], reference[..., channel]
            )  # this is slicing the image and reference along the channel axis
            matched[..., channel] = matched_channel

            # unpacking the source and template values and storing them in the respective dictionaries and setting the histograms
            src_values, src_counts, src_quantiles = source
            tmpl_values, tmpl_counts, tmpl_quantiles = template
            if channel == 0:
                source_cdf["R"] = src_quantiles
                reference_cdf["R"] = tmpl_quantiles

                zip_source = zip(src_values, src_counts)
                source_hist["R"] = dict(zip_source)

                zip_template = zip(tmpl_values, tmpl_counts)
                reference_hist["R"] = dict(zip_template)
            elif channel == 1:
                source_cdf["G"] = src_quantiles
                reference_cdf["G"] = tmpl_quantiles

                zip_source = zip(src_values, src_counts)
                source_hist["G"] = dict(zip_source)

                zip_template = zip(tmpl_values, tmpl_counts)
                reference_hist["G"] = dict(zip_template)

            else:
                source_cdf["B"] = src_quantiles
                reference_cdf["B"] = tmpl_quantiles

                zip_source = zip(src_values, src_counts)
                source_hist["B"] = dict(zip_source)

                zip_template = zip(tmpl_values, tmpl_counts)
                reference_hist["B"] = dict(zip_template)

        return matched, (source_cdf, source_hist), (reference_cdf, reference_hist)
    else:
        matched, source, template = _match_cumulative_cdf(image, reference)

        src_values, src_counts, source_cdf = source
        tmpl_values, tmpl_counts, reference_cdf = template

        zip_source = zip(src_values, src_counts)
        source_hist = dict(zip_source)

        zip_template = zip(tmpl_values, tmpl_counts)
        reference_hist = dict(zip_template)

        return matched, (source_cdf, source_hist), (reference_cdf, reference_hist)


def _match_cumulative_cdf(source, template):
    """This function matches the cumulative distribution function of the source and template images. This is used for histogram matching.

    Args:
        source (ndarray): The source image
        template (ndarray): The reference or template image

    Returns:
        ndarray: The matched image with the same shape as the source image for single channel
        tuple: The source unique intensity values, their counts and the normalized quantiles
        tuple: The template unique intensity values, their counts and the normalized quantiles
    """
    src_values, src_lookup, src_counts = np.unique(
        source.reshape(-1), return_inverse=True, return_counts=True
    )
    tmpl_values, tmpl_counts = np.unique(template.reshape(-1), return_counts=True)

    # calculating the normalized quantiles for each each array
    src_quantiles = np.cumsum(src_counts) / source.size
    tmpl_quantiles = np.cumsum(tmpl_counts) / template.size

    """
    Rounding the quantiles to the nearest integer. Since the pixel values are in the range of 0-255, we will multiply the quantiles with 255 and then round them to the nearest integer.
    """
    src_rounded = np.around(src_quantiles * 255)
    tmpl_rounded = np.around(tmpl_quantiles * 255)  # target histogram

    # now mapping the values for each pixel in the source image. It is mapped to the nearest pixel intensity value based on the template image
    mapped_values = []
    for data in src_rounded:
        # data is that value of pixel whose index is to be found in the tmpl_rounded
        mapped_values.append(_find_nearest_above(tmpl_rounded, data))

    mapped_values = np.array(mapped_values, dtype="uint8")

    # reconstructing the image from the mapped values. The shape of the source image is preserved
    return (
        mapped_values[src_lookup].reshape(source.shape),
        (src_values, src_counts, src_quantiles),
        (tmpl_values, tmpl_counts, tmpl_quantiles),
    )


def _find_nearest_above(tmpl_rounded, target):
    """Finds the nearest value in the tmpl_rounded array which is greater than the target value. This is used for histogram matching.

    Args:
        tmpl_rounded (ndarray): The rounded values of the cumulative distribution function of the template image
        target (int): The target pixel value from the source image

    Returns:
        int: The index of the nearest value of the pixel value in the tmpl_rounded array
    """
    # target is that value of pixel whose index is to be found in the tmpl_rounded
    diff = tmpl_rounded - target

    """
    Creating a mask of the difference array. If the difference is less than or equal to -1, then the mask value will be True, else False. 
    Here's how the mask will look like:
    mask = [True, True, True, True, False,...]
    """
    mask = np.ma.less_equal(diff, -1)

    """
    np.all() returns True if all the values in the mask are True, else False. If all the values are True, then it means that all the values in the tmpl_rounded array are less than the target value. In this case, we will return the index of the nearest value in the tmpl_rounded array. 
    
    There will be one value whose difference will be less than 0. We will find that value and return its index. Since all are in negative. So we will convert the negative values to positive and then find the index of the minimum value.
    
    For eg let's assume:
    tmpl_rounded = [7, 11, 15, 18, 20]
    target = 23
    diff = [-16, -12, -8, -5, -3]
    We need to choose the value which is closest to the target value i.e., value having the minimum difference with the target value
    """
    if np.all(mask):
        c = np.abs(diff).argmin()
        return c

    # If the mask is not all True, then are are some values in the tmpl_rounded array which are greater than the target value. We will find the index of the nearest value in the tmpl_rounded array.
    masked_diff = np.ma.masked_array(
        diff, mask
    )  # this is remove the negative values from the diff array.

    # since negative values are removed, we will return first index of the masked_diff array. This will be the index of the nearest value in the tmpl_rounded array.
    return masked_diff.argmin()
