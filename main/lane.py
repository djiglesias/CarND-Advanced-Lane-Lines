import cv2
import numpy as np

from main.camera import Camera
from main.line import Line
from main.utils import abs_sobel_thresh
from main.utils import mag_thresh
from main.utils import dir_thresh
from main.utils import color_thresh

class Lane():
    def __init__(self, width=50, height=80, margin=100):
        # Class objects.
        self.camera = Camera()
        self.line_left = Line()
        self.line_right = Line()
        
        # Conversions from pixel to real space.
        self.ym_per_pix = 20/350
        self.xm_per_pix = 3.7/1000

        # Line centroid parameters.
        self.window_width = width
        self.window_height = height
        self.margin = margin
        
    def process(self, img):
        """ Augments Lane on Image.
        Returns:
        Image, Original image with lane area overlaid.
        """
        # Extract color & gradient threshold binaries.
        gradx = abs_sobel_thresh(img, orient='x')
        grady = abs_sobel_thresh(img, orient='y')
        mag_binary = mag_thresh(img)
        dir_binary = dir_thresh(img, sobel_kernel=15)
        binary_H, binary_L, binary_S = color_thresh(img)

        # Combine gradient & S channel thresholds.
        combined = np.zeros_like(dir_binary)
        combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1
        combined[(combined == 1) | (binary_S == 1)] = 1

        # Detect Presense of Lane.
        output = self._detect_lane(combined)
        labelled = self._annotate_image(img)
          
        return cv2.addWeighted(labelled, 1, output, 0.3, 0)
    
    def _draw_lane(self, warped):
        """ Draws Lane Line to Image.
        
        Returns:
        Image, Original image with lane overlay.
        """
        # Generate x and y values for plotting
        ploty = np.linspace(0, warped.shape[0]-1, warped.shape[0])        
        left_fitx = self.line_left.get_xfitted(ploty)
        right_fitx = self.line_right.get_xfitted(ploty)
        
        # Draw lane line.
        warp_zero = np.zeros_like(warped).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
        
        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        pts = np.hstack((pts_left, pts_right))
        
        # Draw the lane onto the warped blank image
        cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))
        
        return color_warp
    
    def _detect_lane(self, image):
        """Searchs Image for Possible Lane
        
        Returns:
        Image, Mask of the augmented lane.
        """
        # Apply perspective transform.
        warped = self.camera.warp_image(image)
        
        # Locate Lane Lines & Curvature.
        self._find_lines(warped)
        self._lane_curvature()
        
        # Draw lane and undistort.
        new_lane = self._draw_lane(warped)
        unwarped = self.camera.unwarp_image(new_lane)
        
        return unwarped
    
    def _annotate_image(self, image):
        """Applies Text Headers to Image
        
        Returns:
        Image, Labelled image.
        """
        # Assign text.
        radius = np.average((self.line_left.radius_of_curvature, self.line_right.radius_of_curvature))
        label_radius = "Radius of Curvature ="
        label_value = "%8.1fm" % (radius)
        
        pos_left = self.line_left.current_fit[-1]
        pos_right = self.line_right.current_fit[-1]

        lane_center = (pos_left + pos_right) / 2.0
        image_center = image.shape[1]/2
        pos_center = np.absolute(lane_center - image_center) * self.xm_per_pix

        if lane_center > image_center:
            label_center = "Vehicle is {0:.2f}m left of center.".format(pos_center)
        elif lane_center < image_center:
            label_center = "Vehicle is {0:.2f}m right of center.".format(pos_center)
        else:
            label_center = "Vehicle is centered."
        
        labelled = cv2.putText(image, label_radius, org=(50,60),  fontFace=3, fontScale=2, color=(255,0,0), thickness=3)
        labelled = cv2.putText(image, label_value,  org=(775,60), fontFace=3, fontScale=2, color=(255,0,0), thickness=3)
        labelled = cv2.putText(image, label_center, org=(50,120), fontFace=3, fontScale=2, color=(255,0,0), thickness=3)
    
        return labelled
    
    def _lane_curvature(self):
        """ Detect Radius of Lane Lines
        """       
        # Generate real space curvature.
        y_eval = 720
        
        # Left line.       
        left_fit_cr = np.polyfit(self.line_left.ally*self.ym_per_pix, self.line_left.allx*self.xm_per_pix, 2)
        left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*self.ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
        self.line_left.update_radius(left_curverad)
        
        # Right line.
        right_fit_cr = np.polyfit(self.line_right.ally*self.ym_per_pix, self.line_right.allx*self.xm_per_pix, 2)
        right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*self.ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
        self.line_right.update_radius(right_curverad)

    def _find_lines(self, img, nwindows=9, minpix=50, margin=100):
        """ Finds Lane Lines in Image"""
        
        # Copy image.
        binary_warped = np.copy(img)
        window_height, window_width = self.window_height, self.window_width
        height, width = img.shape[0], img.shape[1]
        margin = self.margin
        
        # Find centroids of image.
        if not (self.line_left.detected & self.line_right.detected):
            # Take a histogram of the bottom half of the image.
            histogram = np.sum(binary_warped[binary_warped.shape[0]//2:,:], axis=0)
            midpoint = np.int(histogram.shape[0]/2)
            
            # Update Base Line.
            self.line_left.update_base(np.argmax(histogram[:midpoint]))
            self.line_right.update_base(np.argmax(histogram[midpoint:]) + midpoint)
            self.window_height = np.int(binary_warped.shape[0]/nwindows)
        
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        
        # Current positions to be updated for each window
        leftx_current = self.line_left.best_base
        rightx_current = self.line_right.best_base
        
        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []
        
        # Create a color mapped image from the binary.
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window+1)*window_height
            win_y_high = binary_warped.shape[0] - window*window_height
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            
            # Draw the windows on the visualization image
            cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(0,255,0), 2)
            cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 2)
            
            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
            (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
            (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
            
            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:        
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

        # Concatenate the arrays of indices
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        # Update polynomial fit.
        self.line_left.update_fit(nonzerox[left_lane_inds], nonzeroy[left_lane_inds])
        self.line_right.update_fit(nonzerox[right_lane_inds], nonzeroy[right_lane_inds]) 
        left_fit = self.line_left.current_fit
        right_fit = self.line_right.current_fit
                
        # Update center positions.
        left_base = left_fit[0]*height**2 + left_fit[1]*height + left_fit[2]
        right_base = right_fit[0]*height**2 + right_fit[1]*height + right_fit[2]
        self.line_left.update_center(np.absolute(width/2 - left_base) * self.xm_per_pix)
        self.line_right.update_center(np.absolute(width/2 - right_base) * self.xm_per_pix)      
        
        