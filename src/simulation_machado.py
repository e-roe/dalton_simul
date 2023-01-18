import numpy as np
import cv2
from PIL import Image
from utils import *
from convert import *

protanomalia_01 = [[0.856167, 0.182038, -0.038205],
                   [0.029342, 0.955115, 0.015544],
                   [-0.002880, -0.001563, 1.004443]]

protanomalia_05 = [[0.458064, 0.679578, -0.137642],
                [0.092785, 0.846313, 0.060902],
                [-0.007494, -0.016807, 1.024301]]

protanomalia_1 = [[0.152286, 1.052583, -0.204868],
                  [0.114503, 0.786281, 0.099216],
                  [-0.003882, -0.048116, 1.051998]]

deuteranomaly_01 = [[0.866435, 0.177704, -0.044139],
                    [0.049567, 0.939063, 0.011370],
                    [-0.003453, 0.007233, 0.996220]]

deuteranomaly_05 = [[0.547494, 0.607765, -0.155259],
                    [0.181692, 0.781742, 0.036566],
                    [-0.010410, 0.027275, 0.983136]]

deuteranomaly_1 = [[0.367322, 0.860646, -0.227968],
                   [0.280085, 0.672501, 0.047413],
                   [-0.011820, 0.042940, 0.968881]]

tritanomaly_01 = [[0.926670, 0.092514, -0.019184],
                  [0.021191, 0.964503, 0.014306],
                  [0.008437, 0.054813, 0.936750]]

tritanomaly_05 = [[1.017277, 0.027029, -0.044306],
                  [-0.006113, 0.958479, 0.047634],
                  [0.006379, 0.248708, 0.744913]]

tritanomaly_1 = [[1.255528, -0.076749, -0.178779],
                 [-0.078411, 0.930809, 0.147602],
                 [0.004733, 0.691367, 0.303900]]

sim_mats = [[protanomalia_01, protanomalia_05, protanomalia_1],
            [deuteranomaly_01, deuteranomaly_05, deuteranomaly_1],
            [tritanomaly_01, tritanomaly_05, tritanomaly_1]]


def daltonize(rgb, color_deficit, severity):

    sim = simulatem(rgb, color_deficit, severity)
    rgb = rgb[..., ::-1].copy()

    sim_rgb = sim.astype(np.float32) / 255.0
    rgb = rgb.astype(np.float32) / 255.0
    print(sim_rgb)

    err2mod = np.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
    # rgb - sim_rgb contains the color information that dichromats
    # cannot see. err2mod rotates this to a part of the spectrum that
    # they can see.
    err = (rgb - sim_rgb) @ err2mod.T
    dtpn = err + rgb
    print(dtpn)
    dtpn = clip_array((dtpn * 255).astype(np.uint8))

    return dtpn

def simulatem(image, cvd, severity):
    im_cv2 = image.copy()
    im_linear_rgb = im_cv2.astype(np.float32) / 255.0
    im_linear_rgb = linearRGB_from_sRGB(im_linear_rgb)
    mat = sim_mats[cvd][severity]
    simul = im_linear_rgb @ np.array(mat).T
    im_cvd_float = sRGB_from_linearRGB(simul)

    return (np.clip(im_cvd_float, 0.0, 1.0) * 255.0).astype(np.uint8)


def find_areas(img_original, img_simulated):

    res_image = img_original.copy()
    img_simulated = cv2.cvtColor(img_simulated, cv2.COLOR_RGB2BGR)
    grayA = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    if len(img_simulated.shape) > 2:
        grayB = cv2.cvtColor(img_simulated, cv2.COLOR_RGB2GRAY)
    else:
        grayB = img_simulated.copy()

    frames_diff = cv2.absdiff(img_original[:,:,2], img_simulated[:,:,2])
    fx = 255 // np.max(frames_diff)
    ret, thresh1 = cv2.threshold(frames_diff * fx, 60, 255, cv2.THRESH_BINARY)

    #cv2.imshow('TH', thresh1)

    thresh1 = cv2.dilate(thresh1, None, iterations=3)
    thresh1 = cv2.erode(thresh1, None, iterations=3)
    # cv2.imshow('TH2', img_original[:,:,2])
    # cv2.imshow('TH3', img_simulated[:,:,2])
    #cv2.waitKey(0)

    # cv2.imshow('OR', img_original)
    # cv2.imshow('SI', img_simulated)

    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cv2.drawContours(res_image, contours, -1, (255, 0, 0), 2)

    return res_image


def find_areas_exp(img_original, img_simulated):
    to_show = False
    res_image = img_original.copy()

    frames_diff_red = cv2.absdiff(img_original[:,:,2], img_simulated[:,:,2])
    #frames_diff_red *= (255 // np.max(frames_diff_red))
    frames_diff_green = cv2.absdiff(img_original[:,:,1], img_simulated[:,:,1])
    #frames_diff_green *= (255 // np.max(frames_diff_green))
    frames_diff_blue = cv2.absdiff(img_original[:,:,1], img_simulated[:,:,1])
    #frames_diff_blue *= (255 // np.max(frames_diff_blue))
    dst_rg = cv2.addWeighted(frames_diff_red, 1, frames_diff_green, 1, 0)
    dst_rgb = cv2.addWeighted(dst_rg, 1, frames_diff_blue, 1, 0)

    # if to_show:
    #     cv2.imshow('diff r', frames_diff_red)
    #     cv2.imshow('diff g', frames_diff_green)
    #     cv2.imshow('diff b', frames_diff_blue)
    #     cv2.imshow('d', dst_rgb)
    #     cv2.waitKey(0)

    ret, thresh1 = cv2.threshold(dst_rgb, 20, 255, cv2.THRESH_BINARY)
    # cv2.imshow('FF', thresh1)
    # cv2.waitKey(0)
    thresh1 = cv2.erode(thresh1, None, iterations=1)
    thresh1 = cv2.dilate(thresh1, None, iterations=1)
    # cv2.imshow('FF', thresh1)
    # cv2.waitKey(0)
    thresh1 = cv2.dilate(thresh1, None, iterations=4)
    thresh1 = cv2.erode(thresh1, None, iterations=4)

    w = 0.6
    dst_f = cv2.addWeighted(res_image, 1-w, cv2.cvtColor(thresh1, cv2.COLOR_GRAY2RGB), w, 0)

    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cv2.drawContours(res_image, contours, -1, (1, 244, 225), -1)
    cv2.drawContours(res_image, contours, -1, (0, 0, 0), 1)
    if to_show:
        cv2.imshow('diff rgb', dst_rgb)
        cv2.imshow('TH', thresh1)
        cv2.imshow('Drw', res_image)
        cv2.imshow('FF', thresh1)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    return dst_f


import sys
if __name__ == "__main__":
    original_image = cv2.imread('D:\\Roe\\Libras\\2022\\conecta\\Color\\imgs\\imA.jpg')
    simu_image = cv2.imread('D:\\Roe\\Libras\\2022\\conecta\\Color\\imgs\\imB.jpg')
    find_areas_exp(original_image, simu_image)
    sys.exit()
    path = '../imgs/webt.jpg'
    type = 1
    serv = 1
    img = cv2.imread(path)
    cv2.imshow('img in', img)
    cv2.waitKey(0)
    res = daltonize(img, type, serv)

    res = res[..., ::-1].copy()
    cv2.imshow('', res)
    cv2.waitKey(0)