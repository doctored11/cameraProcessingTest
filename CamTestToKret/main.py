import cv2

import matplotlib.pyplot as plt
from modules.camScript import Camera, wait_for_camera
from modules.getHist import compute_histogram, initialize_histogram_plot, update_histogram_plot, display_frame_with_histogram
from modules.filters.lowPassFilter import low_pass_filter_gaussian,low_pass_filter_mean, low_pass_filter_bilateral
from modules.cameraAppInterface import create_interface

def main():
    create_interface()



if __name__ == "__main__":
    main()
