'''
This file is part of the domino-detection distribution (https://github.com/jmherzog-de/domino-detection).
Copyright (c) 2021 Adam Mueller and Jean-Marcel Herzog.
  
This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.
 
This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import cv2
import numpy as np

class DominoEyeDetection:

    @staticmethod
    def ExtractEyes(cvImage: np.ndarray, cvOutImage: np.ndarray, min_dist: int, param_1: int, param_2: int, min_radius: int, max_radius: int):

        circles = []

        detected_circles = cv2.HoughCircles(cvImage, method=cv2.HOUGH_GRADIENT, dp=1, minDist=min_dist, param1=param_1, param2=param_2, minRadius=min_radius, maxRadius=max_radius)

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                center_x, center_y, r = pt[0], pt[1], pt[2]
                circles.append({'X': center_x, 'Y': center_y, 'Radius': r})
                cv2.circle(cvOutImage, (center_x,center_y), r, (0, 255, 0), 2)    # draw found circle
                cv2.circle(cvOutImage, (center_x,center_y), 1, (0, 0, 255), 3)    # little circle at the found circle center
        
        return circles
    
    @staticmethod
    def EyeCounting(eyes: list, line_start: tuple, line_end: tuple):
        
        crossproduct = (eyes[1] - line_start[1]) * (line_end[0] - line_start[0]) - (eyes[0] - line_start[0]) * (line_end[1] - line_start[1])
        print(crossproduct)