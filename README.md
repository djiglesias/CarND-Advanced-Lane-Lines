# Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

## 0. The Project

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.
* [Rubric](https://review.udacity.com/#!/rubrics/571/view) for the project.

## 1. Camera Calibration
The camera functionality was abstracted to a class to handle the calibration and perspective transformations of images for this project. For an overview of the code you can view it in main/camera.py. When the Camera class is instantiated the constructor loads a pre-determined image from the 'camera_cal' folder to load the distortion parameters for the camera. Since the camera parameters do not change between sessions, once they are calculated they are saved locally using a pickle database. However, if the database file is not present then all the images from the 'camera_cal' folder are loaded and run through th'cv2.findChessboardCorners()' function to characterize the lense distortion on the camera.

<p align="center">
 <img src="./images/calibration.jpg">
 <img src="./images/corners.jpg">
</p>

Once the corners of the chessboard have been determined, then the distortion on can be applied to an image using the OpenCV 'cv2.calibrateCamera()' function to calculate the parameters (ret, mtx, dist, rvecs, tvecs). The results are then saved using pickle. 

<p align="center">
 <img src="./images/calibration.jpg">
 <img src="./images/test_undist.jpg">
</p>

The camera class has two functions for applying perspective transforms to images to either warp or restore their original shape. These functions will be discussed later in this document.

## 2. Pipeline (Single Images)

### 2.1 Apply Gradient Threshold
...

### 2.2 Apply Color Threshold
...

### 2.3 Combine Thresholds
...

### 2.4 Detect Lane Lines
...

### 2.5 Determine Lane Curvature
...

### 2.7 Unwarp Image & Overlay Lane
...

### 2.8 Annotate Image
...


## 3. Pipeline (Video)
...


## 4. Discussion

### 4.1 Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?


