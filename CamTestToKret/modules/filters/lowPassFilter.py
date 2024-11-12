import cv2
import numpy as np
from scipy.signal import wiener
from scipy.fftpack import fft2, ifft2, fftshift

def low_pass_filter_gaussian(image, kernel_size=3):
    # Применяет размытие Гаусса
    # print("gaus")
    filtered_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return filtered_image

def low_pass_filter_mean(image, kernel_size=5):
    # print("mean")
    # print(kernel_size)

    # Среднее (боксовое) размытие

    filtered_image = cv2.blur(image, (kernel_size, kernel_size))
    return filtered_image

def low_pass_filter_bilateral(image, diameter=9, sigmaColor=75, sigmaSpace=75):
    # Билатеральное размытие
    diameter = int(diameter)

    # print("bil")
    filtered_image = cv2.bilateralFilter(image, diameter, sigmaColor, sigmaSpace)
    return filtered_image

def low_pass_filter_box(image, kernel_size=5):
    # Прямоугольное размытие (аналогично среднему)
    filtered_image = cv2.boxFilter(image, -1, (kernel_size, kernel_size))
    return filtered_image

def low_pass_filter_wiener(image, kernel_size=5):
    # Фильтр Винера
    if image.ndim == 3:
        filtered_image = np.zeros_like(image)
        for i in range(3):
            filtered_image[:, :, i] = wiener(image[:, :, i], (kernel_size, kernel_size))
    else:
        filtered_image = wiener(image, (kernel_size, kernel_size))
    return np.uint8(np.clip(filtered_image, 0, 255))

def low_pass_filter_furie(image, cutoff=0.1):
    # НЧ-фильтр на основе преобразования Фурье
    dft = fft2(image)
    dft_shift = fftshift(dft)

    # Определение размеров и создание круговой маски
    rows, cols = image.shape[:2]
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols), np.uint8)
    r = int(cutoff * min(rows, cols))
    cv2.circle(mask, (ccol, crow), r, 1, thickness=-1)

    # Применение маски
    if image.ndim == 3:
        filtered_image = np.zeros_like(image, dtype=np.float32)
        for i in range(3):
            fshift = dft_shift[:, :, i] * mask
            f_ishift = np.fft.ifftshift(fshift)
            filtered_image[:, :, i] = np.abs(ifft2(f_ishift))
    else:
        fshift = dft_shift * mask
        f_ishift = np.fft.ifftshift(fshift)
        filtered_image = np.abs(ifft2(f_ishift))

    return np.uint8(np.clip(filtered_image, 0, 255))

def low_pass_filter_morf_smooth(image, kernel_size=5):
    # Морфологическое размытие с использованием закрытия
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    filtered_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return filtered_image

def low_pass_filter_bessel(image, cutoff=30):
    # Применение фильтра Бесселя - аппроксимация через Гауссов фильтр (примерный метод)
    bessel_kernel = cv2.getGaussianKernel(cutoff * 2 + 1, -1)
    filtered_image = cv2.sepFilter2D(image, -1, bessel_kernel, bessel_kernel)
    return filtered_image
