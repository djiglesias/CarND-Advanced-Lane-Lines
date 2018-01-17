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
 <img src="./images/calibration.jpg" width=350>
 <img src="./images/corners.jpg" width=350>
</p>

Once the corners of the chessboard have been determined, then the distortion on can be applied to an image using the OpenCV 'cv2.calibrateCamera()' function to calculate the parameters (ret, mtx, dist, rvecs, tvecs). The results are then saved using pickle. 

<p align="center">
 <img src="./images/calibration.jpg" width=350>
 <img src="./images/test_undist.jpg" width=350>
</p>

The camera class has two functions for applying perspective transforms to images to either warp or restore their original shape. These functions will be discussed later in this document.

## 2. Pipeline (Single Images)
The main pipeline for processing the images resides in the Lane class (main/lane.py) which was developed for managing the lane line and camera classes. To augment a lane onto an image, create an instance of class Lane() and pass an RGB image in as an argument to the process() function in the Lane class. This section will explain the steps in the process function.

### 2.1 Apply Thresholds

#### 2.1.1 Magnitude Threshold
Using the Sobel function from OpenCV the change in gradient in both the x and y axes produce binary images indicating the regions of strong gradients which is useful for identifying colored lane lines on a the road. To limit noise on for the Sobel function the RGB image is converted to grayscale and then the magnitude gradient is calculated from the x and y Sobel images by square rooting the sum of the squares of the images. 

<p align="center">
 <img src="./images/straight_lines1.jpg" width=250>
 <img src="./images/L.jpg" width=250>
 <img src="./images/magnitude.jpg" width=250>
</p>

#### 2.1.2 Direction Threshold
...

<p align="center">
 <img src="./images/straight_lines1.jpg" width=250>
 <img src="./images/L.jpg" width=250>
 <img src="./images/direction.jpg" width=250>
</p>

#### 2.1.2 Color Threshold
...

<p align="center">
 <img src="./images/H.jpg" width=250>
 <img src="./images/L.jpg" width=250>
 <img src="./images/S.jpg" width=250>
</p>

#### 2.1.3 Combine Thresholds
...

<p align="center">
 <img src="./images/magnitude.jpg" width=250>
 <img src="./images/direction.jpg" width=250>
 <img src="./images/combined.jpg" width=250>
</p>

<p align="center">
 <img src="./images/combined.jpg" width=250>
 <img src="./images/S.jpg" width=250>
 <img src="./images/s_and_grad.jpg" width=250>
</p>

### 2.2 Detect Lane Lines
...

<p align="center">
 <img src="./images/straight_lines1.jpg" width=250>
 <img src="./images/lane_lines.png" width=250>
 <img src="./images/warped_color.png" width=250>
</p>

<p align="center">
 <img src="./images/histogram.png" width=350>
</p>

<p align="center">
 <img src="./images/sliding_window.png" width=350>
</p>

### 2.3 Determine Lane Curvature
...


### 2.4 Unwarp Image & Overlay Lane
...

<p align="center">
 <img src="./images/lane_find.png" width=250>
 <img src="./images/lane_undsitort.png" width=250>
 <img src="./images/lane_final.png" width=250>
</p>


### 2.5 Annotate Image
...

<p align="center">
 <img src="./images/output_000.jpg" width=250>
 <img src="./images/output_001.jpg" width=250>
 <img src="./images/output_002.jpg" width=250>
 <img src="./images/output_003.jpg" width=250>
 <img src="./images/output_004.jpg" width=250>
 <img src="./images/output_005.jpg" width=250>
</p>

## 3. Pipeline (Video)
...

<p align="center">
 <img src="./videos/p4_smooth.gif" width=600>
</p>

## 4. Discussion

### 4.1 Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?


