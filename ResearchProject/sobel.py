import numpy as np
from scipy.signal import convolve2d

def sobel_filter(image):
    # Sobel filter kernels
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    # Apply Sobel filters to the image along x & y axes
    gx = convolve2d(image, kernel_x, mode='same', boundary='symm')
    gy = convolve2d(image, kernel_y, mode='same', boundary='symm')

    # Calculate gradient magnitude and direction
    gradient_mag = np.sqrt(gx**2 + gy**2)
    gradient_dir = np.arctan2(gy, gx)           #Gradient direction is not being used in our case

    return gradient_mag