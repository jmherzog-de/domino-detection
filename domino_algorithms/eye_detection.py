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

from domino_algorithms.domino_stone import Point

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
    def EyesOnLine(eyes: list, line_start: Point, line_end: Point):
        eyes_on_line = []
        b = Point(0.0, 0.0)
        a = Point(line_start.X, line_start.Y)
        b.X = line_end.X - line_start.X
        b.Y = line_end.Y - line_start.Y
        b_val = np.sqrt(b.X * b.X + b.Y * b.Y)

        # d = |(p-a) x b| / |b|
        # crossproduct = pX * aY - pY * aX

        for eye in eyes:
            d = np.abs(((a.X - eye['X']) * b.Y) - ((a.Y - eye['Y']) * b.X)) / b_val
            print(d)
            if d <= eye['Radius']:
                eyes_on_line.append(eye)
        
        return eyes_on_line

    @staticmethod
    def EyeCounting(stones: list, eyes: list):
        
        for stone in stones:
            stone.Eyes = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Left.Line2[0], stone.ROI_Left.Line2[1])
            print(stone.Eyes)
        
        return