import cv2
import numpy as np

def abs_sobel_thresh(img, orient='x', sobel_kernel=9, thresh=(30, 100)):
    """ Absolute Sobel Threshold Function
    
    Returns:
    Image, image of Sobel function.
    """
    # Grayscale Image.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Calculate Gradient.
    if orient == 'x':
        sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel))
    else:
        sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel))
    
    # Convert to Binary.
    scale_factor = np.max(sobel)/255
    scaled_sobel = (sobel/scale_factor).astype(np.uint8)
    grad_binary = np.zeros_like(scaled_sobel)
    grad_binary[(scaled_sobel >= thresh[0])&(scaled_sobel <= thresh[1])] = 1
    
    # Return the binary image
    return grad_binary

def mag_thresh(image, sobel_kernel=9, mag_thresh=(80, 180)):
    """ Sobel Magnitude Threshold Function
    
    Returns:
    Image, magnitude of Sobel gradients.
    """
    # Convert to Grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Take both Sobel x and y gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    
    # Calculate the gradient magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    
    # Rescale to 8 bit
    scale_factor = np.max(gradmag)/255 
    gradmag = (gradmag/scale_factor).astype(np.uint8)
    
    # Create a binary image of ones where threshold is met, zeros otherwise
    mag_binary = np.zeros_like(gradmag)
    mag_binary[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1
    
    # Return the binary image
    return mag_binary

def dir_thresh(image, sobel_kernel=9, thresh=(0.7, 1.3)):
    """ Compute the Directional Threshold
    
    Returns:
    Image, Binary image of original.
    """
    # Grayscale Image.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate the x and y gradients.
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    
    # Take the absolute value of the gradient direction.
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    binary_output =  np.zeros_like(absgraddir)
    binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1

    # Return the binary image
    return binary_output

def color_thresh(img, thresh_H=(15, 30), thresh_L=(130, 180), thresh_S=(180, 255)):
    """Color Threshold Mask
    
    Returns:
    Image, binary image of color.
    """
    # Convert image to HLS spectrum.
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    H = hls[:,:,0]
    L = hls[:,:,1]
    S = hls[:,:,2]
    
    # Create binary masks for each spectrum.
    binary_H = np.zeros_like(H)
    binary_L = np.zeros_like(L)
    binary_S = np.zeros_like(S)
    binary_H[(H > thresh_H[0])&(H <= thresh_H[1])] = 1
    binary_L[(L > thresh_L[0])&(L <= thresh_L[1])] = 1
    binary_S[(S > thresh_S[0])&(S <= thresh_S[1])] = 1
    
    return binary_H, binary_L, binary_S