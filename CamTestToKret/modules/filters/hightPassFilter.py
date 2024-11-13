#ВЧФ
#тоже штук 5-8


import cv2
import numpy as np

# todo собрать фильтров 5-10
#тоже проверить - это так для тестов
def high_pass_filter_laplacian(image, kernel_size=3):


    laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=kernel_size)
    laplacian = cv2.convertScaleAbs(laplacian)
    return laplacian

def high_pass_filter_sobel(image, kernel_size=3):

    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)
    sobel = cv2.magnitude(sobel_x, sobel_y)
    sobel = cv2.convertScaleAbs(sobel)
    return sobel

def high_pass_filter_unsharp_mask(image, sigma=1.0, strength=1.5):

    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    high_pass = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return high_pass
