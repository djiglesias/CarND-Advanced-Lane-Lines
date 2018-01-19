import numpy as np

class Line():
    def __init__(self):
        
        self.detected = False  
        self.recent_xfitted = []
        self.current_fit = [np.array([False])]
        self.radius_of_curvature = None
        self.line_base_pos = None 
        self.allx = None  
        self.ally = None
        self.base = []
        self.best_base = None
        
    def get_xfitted(self, ploty):
        """Updates Recent X Fitted Points
        Returns:
        Int[], all xfitted points.
        """
        if self.detected:
            A = self.current_fit[0]
            B = self.current_fit[1]
            C = self.current_fit[2]
            self.recent_xfitted = A*ploty**2 + B*ploty + C
        
        return self.recent_xfitted
    
    def update_base(self, base):
        """Updates Base X Pixel"""
        self.detected = True
        if self.best_base is None:
            self.base.append(base)
            self.best_base = base            
        elif abs(self.best_base - base) > 50:
            self.detected = False
        else:
            self.base.append(base)
            if len(self.base) > 10:
                self.base.pop(0)
            self.best_base = sum(self.base)/len(self.base)
            
    def update_fit(self, allx, ally):
        """Updates Polynomial Fit"""
        
        self.detected = True
        
        if len(allx) > 10:
            fit = np.polyfit(ally, allx, 2)
        
            # Update current fit coefficients.
            if not self.current_fit[0]:
                self.current_fit = fit
                self.allx = allx
                self.ally = ally
            else:
                threshold = True      
                diff = self.current_fit/fit
                
                for i, coeff in enumerate(fit):
                    if (diff[i] < 0.20) | (diff[i] > 2.5):
                        threshold = False
                        
                if threshold:
                    self.allx = allx
                    self.ally = ally
                self.current_fit = self.current_fit*0.60 + fit*0.40    
        else:
            self.detected = False        
                
    def update_center(self, pos):
        """Updates Lane Center"""
        if self.line_base_pos is None:
            self.line_base_pos = pos
        else:
            self.line_base_pos = self.line_base_pos*0.70 + pos*0.30
        
    def update_radius(self, radius):
        """Updates Lane Curvature"""
        if radius > 5000.0:
            radius = 5000.0
        
        if self.radius_of_curvature is None:
            self.radius_of_curvature = radius
        else:
            self.radius_of_curvature = self.radius_of_curvature*0.95 + radius*0.05