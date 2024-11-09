import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_histogram(image):
    if len(image.shape) == 3:
        channels = ('b', 'g', 'r')
        histograms = {}
        for i, col in enumerate(channels):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            histograms[col] = hist
        return histograms
    else:
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        return {"gray": hist}

def initialize_histogram_plot():
    fig, ax = plt.subplots()
    line_r, = ax.plot(np.zeros(256), 'r', label="Red")
    line_g, = ax.plot(np.zeros(256), 'g', label="Green")
    line_b, = ax.plot(np.zeros(256), 'b', label="Blue")
    ax.set_xlim([0, 256])
    ax.set_ylim([0, 10000])
    ax.legend()
    return fig, ax, line_r, line_g, line_b

def update_histogram_plot(line_r, line_g, line_b, histograms):
    line_r.set_ydata(histograms['r'])
    line_g.set_ydata(histograms['g'])
    line_b.set_ydata(histograms['b'])

def display_frame_with_histogram(frame, line_r, line_g, line_b):
    histograms = compute_histogram(frame)
    update_histogram_plot(line_r, line_g, line_b, histograms)
