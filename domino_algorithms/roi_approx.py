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


def calculate_points(center_x: int, center_y: int, angle: float, offset: float):
    
    sin     = np.sin(angle * 3.1415 / 180.0)
    cos     = np.cos(angle * 3.1415 / 180.0)

    if angle > 5.0:
        ps_y = center_y - offset * sin
        ps_x = center_x + offset * cos
    else:
        ps_y = center_y + offset
        ps_x = center_x
    return np.int32(np.round(ps_x)), np.int32(np.round(ps_y))


class RoiApprox:

    @staticmethod
    def FindROI(dividers: list, cvOutImage: np.ndarray, stone_length: int = 150):
        
        for divider in dividers:
            
            #
            # Extract divider center points and convert them into decimals
            # Note: this is needed to draw the center line.
            #
            p1_x = np.int32(np.round(divider['center'][0]))
            p1_y = np.int32(np.round(divider['center'][1]))
            

            #
            # Calculate right side of the second detection row
            #
            #ps_x, ps_y = calculate_points(p1_x, p1_y, divider['angle'], offset=25.0)
            #p2_x       = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos(divider['angle'] * 3.1415 / 180.0)))
            #p2_y       = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin(divider['angle'] * 3.1415 / 180.0)))
            #cv2.line(cvOutImage, (ps_x, ps_y), (p2_x, p2_y), color=(255,255,0), thickness=2)

            #
            # Calculate left side of the second detection row
            #
            #p2_x       = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos(divider['angle'] * 3.1415 / 180.0)))
            #p2_y       = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin(divider['angle'] * 3.1415 / 180.0)))
            #cv2.line(cvOutImage, (ps_x, ps_y), (p2_x, p2_y), color=(255,255,0), thickness=2)

            #
            # Calculate right side of the first detection row
            #
            #ps_x, ps_y = calculate_points(p1_x, p1_y, divider['angle'], offset=-25.0)
            #p2_x       = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos(divider['angle'] * 3.1415 / 180.0)))
            #p2_y       = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin(divider['angle'] * 3.1415 / 180.0)))
            #cv2.line(cvOutImage, (ps_x, ps_y), (p2_x, p2_y), color=(255,255,0), thickness=2)

            #
            # Calculate left side of the first detection row
            #
            #p2_x       = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos(divider['angle'] * 3.1415 / 180.0)))
            #p2_y       = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin(divider['angle'] * 3.1415 / 180.0)))
            #cv2.line(cvOutImage, (ps_x, ps_y), (p2_x, p2_y), color=(255,255,0), thickness=2)

            #
            # Calculate right side of the center line
            #
            p2_x = np.int32(np.round(divider['center'][0] + stone_length * 0.5 * np.cos(divider['angle'] * 3.1415 / 180.0)))
            p2_y = np.int32(np.round(divider['center'][1] + stone_length * 0.5 * np.sin(divider['angle'] * 3.1415 / 180.0)))
            cv2.line(cvOutImage, (p1_x, p1_y), (p2_x, p2_y), color=(255,0,0), thickness=2)

            #
            # Calculate the left side of the center line
            #
            p2_x = np.int32(np.round(divider['center'][0] - stone_length * 0.5 * np.cos(divider['angle'] * 3.1415 / 180.0)))
            p2_y = np.int32(np.round(divider['center'][1] - stone_length * 0.5 * np.sin(divider['angle'] * 3.1415 / 180.0)))
            cv2.line(cvOutImage, (p1_x, p1_y), (p2_x, p2_y), color=(0,255,0), thickness=2)

            

            
            

            