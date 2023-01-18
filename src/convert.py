
import numpy as np


def linearRGB_from_sRGB(im):
    # https://github.com/DaltonLens/DaltonLens-Python/blob/master/daltonlens/convert.py
    """Convert sRGB to linearRGB, removing the gamma correction.

    Formula taken from Wikipedia https://en.wikipedia.org/wiki/SRGB

    Parameters
    ==========
    im : array of shape (M,N,3) with dtype float
        The input sRGB image, normalized between [0,1]

    Returns
    =======
    im : array of shape (M,N,3) with dtype float
        The output RGB image
    """
    out = np.zeros_like(im)
    small_mask = im < 0.04045
    large_mask = np.logical_not(small_mask)
    out[small_mask] = im[small_mask] / 12.92
    out[large_mask] = np.power((im[large_mask] + 0.055) / 1.055, 2.4)
    return out


def sRGB_from_linearRGB(im):
    """Convert linearRGB to sRGB, applying the gamma correction.

    Formula taken from Wikipedia https://en.wikipedia.org/wiki/SRGB

    Parameters
    ==========
    im : array of shape (M,N,3) with dtype float
        The input RGB image, normalized between [0,1].
        It will be clipped to [0,1] to avoid numerical issues with gamma.

    Returns
    =======
    im : array of shape (M,N,3) with dtype float
        The output sRGB image
    """
    out = np.zeros_like(im)
    # Make sure we're in range, otherwise gamma will go crazy.
    im = np.clip(im, 0., 1.)
    small_mask = im < 0.0031308
    large_mask = np.logical_not(small_mask)
    out[small_mask] = im[small_mask] * 12.92
    out[large_mask] = np.power(im[large_mask], 1.0 / 2.4) * 1.055 - 0.055
    return out

