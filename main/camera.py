import cv2
import glob
import numpy as np
import pickle

class Camera():
    
    def __init__(self, filename='camera_cal/calibration1.jpg', nx=9, ny=6):
        self.objpoints = []
        self.imgpoints = []
        self.nx = nx
        self.ny = ny
        self.mtx = None
        self.dist = None
        self.M = None
        self.Minv = None
        
        # Load calibration settings.
        self._calibrate(filename)

    def _calibrate(self, filename):
        """ Calibrate the camera."""
        img = cv2.imread(filename)
        self._get_distortion(img)
        
        
    def _calibrate_camera(self, filepath='camera_cal/calibration*.jpg'):
        """ Camera Calibration."""

        # Load calibration images.
        images = glob.glob(filepath)
        objp = np.zeros((nx*ny,3), np.float32)
        objp[:,:2] = np.mgrid[0:self.nx, 0:self.ny].T.reshape(-1,2)

        # Pass through all images.
        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)
            if ret == True: 
                self.objpoints.append(objp)
                self.imgpoints.append(corners)

    def _get_distortion(self, img, filename='camera_cal/wide_dist_pickle.p'):
        """ Saves distortion matrix."""
        try:
            dist_pickle = pickle.load(open(filename, "rb"))
            self.mtx = dist_pickle["mtx"]
            self.dist = dist_pickle["dist"]
        except:
            self.objpoints, self.imgpoints = self._calibrate_camera()
            img_size = (img.shape[1], img.shape[0])
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, img_size, None, None)
            dst = cv2.undistort(img, self.mtx, self.dist, None, self.mtx)

            # Save the camera calibration result for later use.
            dist_pickle = {}
            dist_pickle["mtx"] = self.mtx
            dist_pickle["dist"] = self.dist
            pickle.dump( dist_pickle, open( filename, "wb" ) )

    def warp_image(self, img):
        """Warp Image
        
        Returns:
        Image, top-down view of original image.
        """
        # Undistort the image.
        undist = cv2.undistort(img, self.mtx, self.dist, None, self.mtx)

        # Define lane region with lines.
        corners = [[580, 455],[695, 455],[1060, 690],[250, 690]]

        # Define src and dst regions.
        src = np.float32([corners[0], corners[1], corners[2], corners[3]])
        offset = [200, 30]
        img_size = (img.shape[1], img.shape[0])
        dst = np.float32([[offset[0], offset[1]], 
                          [img_size[0]-offset[0], offset[1]], 
                          [img_size[0]-offset[0], img_size[1]-offset[1]], 
                          [offset[0], img_size[1]-offset[1]]])
        self.M = cv2.getPerspectiveTransform(src, dst)
        self.Minv = cv2.getPerspectiveTransform(dst, src)

        return cv2.warpPerspective(undist, self.M, img_size)
    
    def unwarp_image(self, img):
        """ Unwarp Image to Original
        Returns:
        Image, unwarped image of original.
        """
        img_size = (img.shape[1], img.shape[0])
        return cv2.warpPerspective(img, self.Minv, img_size, flags=cv2.INTER_LINEAR)