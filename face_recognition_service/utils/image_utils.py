import math

import cv2
import numpy as np




def calculate_distance_on_landmark(landmark, start, end):
    x_s, y_s = landmark[start]
    x_e, y_e = landmark[end]
    return math.dist((x_s, y_s), (x_e, y_e))




def calculate_summed_area(integral_image, x1, y1, x2, y2):
    x1 += 1
    y1 += 1
    x2 += 1
    y2 += 1
    A = np.int64(integral_image[y1 - 1][x1 - 1])
    B = np.int64(integral_image[y1 - 1][x2])
    C = np.int64(integral_image[y2][x1 - 1])
    D = np.int64(integral_image[y2][x2])

    return D + A - C - B
