import numpy as np


def gammar(rgb, gamma=2.4):
    linear_rgb = np.zeros_like(rgb, dtype=np.float16)
    for i in range(3):
        linear_rgb[:, :, i] = (rgb[:, :, i] / 255) ** gamma

    return linear_rgb


def gamma_correction(s_rgb, gamma=2.4):
    linear_rgb = np.zeros_like(s_rgb, dtype=np.float16)
    for i in range(s_rgb.shape[2]):
        idx = s_rgb[:, :, i] > 0.04045 * 255
        linear_rgb[idx, i] = ((s_rgb[idx, i] / 255 + 0.055) / 1.055) ** gamma
        idx = np.logical_not(idx)
        linear_rgb[idx, i] = s_rgb[idx, i] / 255 / 12.92

    return linear_rgb


def inverse_gamma_correction(linear_rgb, gamma=2.4):
    rgb = np.zeros_like(linear_rgb, dtype=np.float16)
    for i in range(3):
        idx = linear_rgb[:, :, i] <= 0.0031308
        rgb[idx, i] = 255 * 12.92 * linear_rgb[idx, i]
        idx = np.logical_not(idx)
        rgb[idx, i] = 255 * (1.055 * linear_rgb[idx, i]**(1/gamma) - 0.055)

    return np.round(rgb)


def sRGB_from_linearRGB(v):
    if v <= 0.:
        return 0
    if v >= 1.:
        return 255
    if v < 0.0031308:
        return 0.5 + (v * 12.92 * 255)

    return 255 * (pow(v, 1.0 / 2.4) * 1.055 - 0.055)


def clip_array(arr):
    comp_arr = np.ones_like(arr)
    arr = np.maximum(comp_arr * 0, arr)
    arr = np.minimum(comp_arr * 255, arr)

    return arr