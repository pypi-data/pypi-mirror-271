from imgcv.common import check_image
import numpy as np
from warnings import warn


def histogram_equalization(img):
    """Equalizes the histogram of the image and returns the equalized image.

    Args:
        img (np.ndarray): Image to equalize the histogram

    Returns:
        np.ndarray: Equalized image
    """

    check_image(img)

    pixel_freqs = calculate_histogram(img)
    pdf = calculate_pdf(img, pixel_freqs)
    cdf = calculate_cdf(img, pdf)

    if img.ndim == 2:
        equi_hist = {}

        for key in cdf:
            equi_hist[key] = round(cdf[key] * 255)

        equ_im = np.zeros(img.shape)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                equ_im[i][j] = equi_hist[img[i][j]]

    elif img.ndim == 3:
        equi_hist = {"R": {}, "G": {}, "B": {}}

        for key in cdf["R"]:
            equi_hist["R"][key] = round(cdf["R"][key] * 255)

        for key in cdf["G"]:
            equi_hist["G"][key] = round(cdf["G"][key] * 255)

        for key in cdf["B"]:
            equi_hist["B"][key] = round(cdf["B"][key] * 255)

        equ_im = np.zeros(img.shape)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                equ_im[i][j][0] = equi_hist["R"][img[i][j][0]]
                equ_im[i][j][1] = equi_hist["G"][img[i][j][1]]
                equ_im[i][j][2] = equi_hist["B"][img[i][j][2]]

    return equ_im.astype(np.uint8), equi_hist


def calculate_histogram(img):
    """Calculates the histogram of the image

    Args:
        img (np.ndarrray): Image to calculate the histogram

    Returns:
        dict: Dictionary containing the frequency of each pixel value
    """
    check_image(img)

    # creating dictionary to store the frequency of each pixel value

    if img.ndim == 3:
        # For each channel we will have a dictionary
        pixel_freq = {"R": {}, "G": {}, "B": {}}

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j][0] in pixel_freq["R"]:
                    pixel_freq["R"][img[i][j][0]] += 1
                else:
                    pixel_freq["R"][img[i][j][0]] = 1

                if img[i][j][1] in pixel_freq["G"]:
                    pixel_freq["G"][img[i][j][1]] += 1
                else:
                    pixel_freq["G"][img[i][j][1]] = 1

                if img[i][j][2] in pixel_freq["B"]:
                    pixel_freq["B"][img[i][j][2]] += 1
                else:
                    pixel_freq["B"][img[i][j][2]] = 1

        pixel_freq["R"] = dict(sorted(pixel_freq["R"].items()))
        pixel_freq["G"] = dict(sorted(pixel_freq["G"].items()))
        pixel_freq["B"] = dict(sorted(pixel_freq["B"].items()))

    elif img.ndim == 2:
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

    if img.ndim == 2:
        total_pixels = img.size
        # probability density function
        pdf = {}

        for key in pixel_freqs:
            pdf[key] = np.round(pixel_freqs[key] / total_pixels, 4)

    elif img.ndim == 3:
        total_pixels = img.size // 3
        pdf = {"R": {}, "G": {}, "B": {}}

        for key in pixel_freqs["R"]:
            pdf["R"][key] = np.round(pixel_freqs["R"][key] / total_pixels, 4)

        for key in pixel_freqs["G"]:
            pdf["G"][key] = np.round(pixel_freqs["G"][key] / total_pixels, 4)

        for key in pixel_freqs["B"]:
            pdf["B"][key] = np.round(pixel_freqs["B"][key] / total_pixels, 4)

    return pdf


def calculate_cdf(img, pdf):
    """Calculates the cumulative density function of the image

    Args:
        img (np.ndarray): Image to calculate the cdf
        pdf (dict): Dictionary containing the probability density function of the image

    Returns:
        dict: Dictionary containing the cumulative density function of the image
    """

    check_image(img)

    if img.ndim == 2:
        cdf = {}

        # each cdf is the sum of current pdf + previous cdf
        for i, key in enumerate(pdf):
            # if it is the first value
            if i == 0:
                cdf[key] = pdf[key]
            else:
                # this is taking the previous cdf value and adding the current pdf value
                cdf[key] = cdf[list(cdf.keys())[i - 1]] + pdf[key]

    elif img.ndim == 3:
        cdf = {"R": {}, "G": {}, "B": {}}

        for i, key in enumerate(pdf["R"]):
            if i == 0:
                cdf["R"][key] = pdf["R"][key]
            else:
                cdf["R"][key] = cdf["R"][list(cdf["R"].keys())[i - 1]] + pdf["R"][key]

        for i, key in enumerate(pdf["G"]):
            if i == 0:
                cdf["G"][key] = pdf["G"][key]
            else:
                cdf["G"][key] = cdf["G"][list(cdf["G"].keys())[i - 1]] + pdf["G"][key]

        for i, key in enumerate(pdf["B"]):
            if i == 0:
                cdf["B"][key] = pdf["B"][key]
            else:
                cdf["B"][key] = cdf["B"][list(cdf["B"].keys())[i - 1]] + pdf["B"][key]

    return cdf
