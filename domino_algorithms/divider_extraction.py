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
import math

from domino_algorithms.domino_stone import DominoStone

class DividerExtraction:

    @staticmethod
    def ExtractDividers(cvImage: np.ndarray, minArea: int, cvOutImage: np.ndarray):
        
        
        domino_stones = list()

        #
        # Find Contours
        #    
        contours,_ = cv2.findContours(cvImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)   
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < minArea:
                continue

            eps = 0.05 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(curve=cnt, epsilon=eps, closed=True)
            
            # get rotated rectangle from contour
            rot_rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rot_rect)
            box = np.int0(box)
            

            # get dimensions
            (center), (width, height), angle = rot_rect

            
            # get the center line from box
            # note points are clockwise from bottom right
            if width > height:
                x1 = (box[0][0] + box[1][0]) // 2
                y1 = (box[0][1] + box[1][1]) // 2
                x2 = (box[3][0] + box[2][0]) // 2
                y2 = (box[3][1] + box[2][1]) // 2
            else:
                x1 = (box[0][0] + box[3][0]) // 2
                y1 = (box[0][1] + box[3][1]) // 2
                x2 = (box[1][0] + box[2][0]) // 2
                y2 = (box[1][1] + box[2][1]) // 2

            
            # compute center line length
            cl_length = math.sqrt( (x1-x2)**2 + (y1-y2)**2)

            domino_stones.append(DominoStone(center_x=center[0], center_y=center[1], length=cl_length, width=width, height=height, angle_deg=angle))
                                    
            cv2.drawContours(cvOutImage, [box], 0, (255, 255, 255), 1)

            # draw centerline on image
            cv2.line(cvOutImage, pt1=(x1, y1), pt2=(x2, y2), color=(0, 0, 255), thickness=2)
            cv2.line(cvOutImage, pt1=(x1, y1), pt2=(x2, y2), color=(0, 0, 255), thickness=2)
          

        return domino_stones