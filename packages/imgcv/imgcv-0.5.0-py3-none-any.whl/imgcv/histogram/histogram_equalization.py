from imgcv.common import check_image
import numpy as np
from warnings import warn


def histogram_equalization(img):
    """Equalizes the histogram of the image and returns the equalized image.

    Note: This function currently only works for grayscale images.

    Args:
        img (np.ndarray): Image to equalize the histogram

    Returns:
        np.ndarray: Equalized image
    """

    check_image(img)

    pixel_freqs = calculate_histogram(img)
    pdf = calculate_pdf(img, pixel_freqs)
    cdf = calculate_cdf(img, pdf)

    equi_hist = {}

    for key in cdf:
        equi_hist[key] = round(cdf[key] * 255)

    equ_im = np.zeros(img.shape)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            equ_im[i][j] = equi_hist[img[i][j]]

    return equ_im, equi_hist


def calculate_histogram(img):
    """Calculates the histogram of the image

    Note: This function currently only works for grayscale images.

    Args:
        img (np.ndarrray): Image to calculate the histogram

    Returns:
        dict: Dictionary containing the frequency of each pixel value
    """
    check_image(img)

    # creating dictionary to store the frequency of each pixel value
    pixel_freq = {}

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] in pixel_freq:
                pixel_freq[img[i][j]] += 1
            else:
                pixel_freq[img[i][j]] = 1

    pixel_freq = dict(sorted(pixel_freq.items()))

    return pixel_freq


def calculate_pdf(img, pixel_freqs):
    """Calculates the probability density function of the image

    Note: This function currently only works for grayscale images.

    Args:
        img (np.ndarray): Image to calculate the pdf
        pixel_freqs (dict): Dictionary containing the frequency of each pixel value

    Returns:
        dict: Dictionary containing the probability density function of the image
    """
    check_image(img)

    check_image(img)

    total_pixels = img.shape[0] * img.shape[1]

    # probability density function
    pdf = {}

    for key in pixel_freqs:
        pdf[key] = np.round(pixel_freqs[key] / total_pixels, 4)

    return pdf


def calculate_cdf(img, pdf):
    """Calculates the cumulative density function of the image

    Note: This function currently only works for grayscale images.

    Args:
        img (np.ndarray): Image to calculate the cdf
        pdf (dict): Dictionary containing the probability density function of the image

    Returns:
        dict: Dictionary containing the cumulative density function of the image
    """

    check_image(img)

    # cumulative density function
    cdf = {}

    # each cdf is the sum of current pdf + previous cdf
    for i, key in enumerate(pdf):
        # if it is the first value
        if i == 0:
            cdf[key] = pdf[key]
        else:
            # this is taking the previous cdf value and adding the current pdf value
            cdf[key] = cdf[list(cdf.keys())[i - 1]] + pdf[key]

    return cdf
