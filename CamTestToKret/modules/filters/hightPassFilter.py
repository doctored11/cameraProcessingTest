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


def high_pass_filter_gradient(image, kernel_size=3):
    # вроде его просили
    # Градиентный фильтр: вычисляет разницу интенсивностей по строкам и столбцам, затем суммирует.

    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1,  ksize=kernel_size)
    gradient = cv2.addWeighted(cv2.convertScaleAbs(gradient_x), 0.5,
                               cv2.convertScaleAbs(gradient_y), 0.5, 0)
    return gradient

def high_pass_filter_laplacian_second_order(image, kernel_size=3):
    laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=kernel_size)
    laplacian_second_order = cv2.Laplacian(laplacian, cv2.CV_64F, ksize=kernel_size)
    return cv2.convertScaleAbs(laplacian_second_order)



def high_pass_filter_scharr(image):
    scharr_x = cv2.Scharr(image, cv2.CV_64F, 1, 0)
    scharr_y = cv2.Scharr(image, cv2.CV_64F, 0, 1)
    scharr = cv2.magnitude(scharr_x, scharr_y)
    return cv2.convertScaleAbs(scharr)


def high_pass_filter_prewitt(image):
    kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
    kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

    prewitt_x = cv2.filter2D(image, cv2.CV_64F, kernelx)
    prewitt_y = cv2.filter2D(image, cv2.CV_64F, kernely)

    prewitt = cv2.magnitude(prewitt_x, prewitt_y)
    return cv2.convertScaleAbs(prewitt)
