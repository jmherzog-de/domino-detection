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
    def FindROI(stones: list, cvOutImage: np.ndarray, stone_length: int = 250, offset: int = 40):
        
        for stone in stones:

            # Extract divider center points and convert them into decimals
            # Note: this is needed to draw the center line.
            p1_x = np.int32(np.round(stone.Center.X))
            p1_y = np.int32(np.round(stone.Center.Y))

            stone.ROI_Right.Line2[0]    = Point(p1_x, p1_y)
            stone.ROI_Left.Line2[0]     = Point(p1_x, p1_y)
                        
            if stone.Angle >= 88.0 and stone.Angle <= 92.0 and stone.Width < stone.Height:
                
                stone.ROI_Right.Line1[0].X = p1_x - offset
                stone.ROI_Right.Line1[0].Y = p1_y

                stone.ROI_Right.Line1[1].X = p1_x - offset
                stone.ROI_Right.Line1[1].Y = np.int32(p1_y + stone_length * 0.5)

                stone.ROI_Left.Line1[0].X = p1_x - offset
                stone.ROI_Left.Line1[0].Y = p1_y

                stone.ROI_Left.Line1[1].X = p1_x - offset
                stone.ROI_Left.Line1[1].Y = np.int32(p1_y - stone_length * 0.5)

                stone.ROI_Right.Line2[1].X = p1_x
                stone.ROI_Right.Line2[1].Y = np.int32(np.round(stone.Center.Y + stone_length * 0.5))

                stone.ROI_Left.Line2[1].X = p1_x
                stone.ROI_Left.Line2[1].Y = np.int32(np.round(stone.Center.Y - stone_length * 0.5))

                stone.ROI_Right.Line3[0].X = p1_x + offset
                stone.ROI_Right.Line3[0].Y = p1_y
                
                stone.ROI_Right.Line3[1].X = p1_x + offset
                stone.ROI_Right.Line3[1].Y = np.int32(p1_y + stone_length * 0.5)

                stone.ROI_Left.Line3[0].X = p1_x + offset
                stone.ROI_Left.Line3[0].Y = p1_y
                
                stone.ROI_Left.Line3[1].X = p1_x + offset
                stone.ROI_Left.Line3[1].Y = np.int32(p1_y - stone_length * 0.5)

            elif stone.Angle >= 88.0 and stone.Angle <= 92.0:

                stone.ROI_Right.Line1[0].X = p1_x
                stone.ROI_Right.Line1[0].Y = p1_y + offset

                stone.ROI_Right.Line1[1].X = np.int32(p1_x + stone_length * 0.5)
                stone.ROI_Right.Line1[1].Y = p1_y + offset

                stone.ROI_Left.Line1[0].X = p1_x
                stone.ROI_Left.Line1[0].Y = p1_y + offset

                stone.ROI_Left.Line1[1].X = np.int32(p1_x - stone_length * 0.5)
                stone.ROI_Left.Line1[1].Y = p1_y + offset

                stone.ROI_Right.Line2[1].X = np.int32(np.round(stone.Center.X + stone_length * 0.5))
                stone.ROI_Right.Line2[1].Y = p1_y

                stone.ROI_Left.Line2[1].X = np.int32(np.round(stone.Center.X - stone_length * 0.5))
                stone.ROI_Left.Line2[1].Y = p1_y

                stone.ROI_Right.Line3[0].X = p1_x
                stone.ROI_Right.Line3[0].Y = p1_y - offset
                
                stone.ROI_Right.Line3[1].X = np.int32(p1_x + stone_length * 0.5)
                stone.ROI_Right.Line3[1].Y = p1_y - offset

                stone.ROI_Left.Line3[0].X = p1_x
                stone.ROI_Left.Line3[0].Y = p1_y - offset
                
                stone.ROI_Left.Line3[1].X = np.int32(p1_x - stone_length * 0.5)
                stone.ROI_Left.Line3[1].Y = p1_y - offset

            elif stone.Height > stone.Width:
                
                # calculate first detection row
                ps_x, ps_y = calculate_points(p1_x, p1_y, 90.0 - stone.Angle, offset)
                stone.ROI_Right.Line1[0]    = Point(ps_x, ps_y)
                stone.ROI_Right.Line1[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
                stone.ROI_Right.Line1[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))
                stone.ROI_Left.Line1[0]     = Point(ps_x, ps_y)
                stone.ROI_Left.Line1[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
                stone.ROI_Left.Line1[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))

                # calculate second detection row (center)
                stone.ROI_Right.Line2[0]    = Point(p1_x, p1_y)
                stone.ROI_Right.Line2[1].X  = np.int32(np.round(stone.Center.X + stone_length * 0.5 * np.cos((stone.Angle) * 3.1415 / 180.0)))
                stone.ROI_Right.Line2[1].Y  = np.int32(np.round(stone.Center.Y + stone_length * 0.5 * np.sin((stone.Angle) * 3.1415 / 180.0)))
                stone.ROI_Left.Line2[0]     = Point(p1_x, p1_y)
                stone.ROI_Left.Line2[1].X   = np.int32(np.round(stone.Center.X - stone_length * 0.5 * np.cos((stone.Angle) * 3.1415 / 180.0)))
                stone.ROI_Left.Line2[1].Y   = np.int32(np.round(stone.Center.Y - stone_length * 0.5 * np.sin((stone.Angle) * 3.1415 / 180.0)))

                # calculate third detection row
                ps_x, ps_y                  = calculate_points(p1_x, p1_y, 90.0-stone.Angle, offset=-1*offset)
                stone.ROI_Right.Line3[0]    = Point(ps_x, ps_y)
                stone.ROI_Right.Line3[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
                stone.ROI_Right.Line3[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))
                stone.ROI_Left.Line3[0]     = Point(ps_x, ps_y)
                stone.ROI_Left.Line3[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
                stone.ROI_Left.Line3[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))

            else:

                # calculate first detection row
                ps_x, ps_y = calculate_points(p1_x, p1_y, 180.0 - stone.Angle, offset)
                stone.ROI_Right.Line1[0]    = Point(ps_x, ps_y)
                stone.ROI_Right.Line1[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
                stone.ROI_Right.Line1[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin((stone.Angle + 90.0 )* 3.1415 / 180.0)))
                stone.ROI_Left.Line1[0]     = Point(ps_x, ps_y)
                stone.ROI_Left.Line1[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
                stone.ROI_Left.Line1[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

                # calculate second detection row (center)
                calc_angle = stone.Angle + 90.0
                stone.ROI_Right.Line2[1].X  = np.int32(np.round(stone.Center.X + stone_length * 0.5 * np.cos((calc_angle) * 3.1415 / 180.0)))
                stone.ROI_Right.Line2[1].Y  = np.int32(np.round(stone.Center.Y + stone_length * 0.5 * np.sin((calc_angle) * 3.1415 / 180.0)))
                stone.ROI_Left.Line2[1].X   = np.int32(np.round(stone.Center.X - stone_length * 0.5 * np.cos((calc_angle) * 3.1415 / 180.0)))
                stone.ROI_Left.Line2[1].Y   = np.int32(np.round(stone.Center.Y - stone_length * 0.5 * np.sin((calc_angle) * 3.1415 / 180.0)))

            
                # calculate third detection row
                ps_x, ps_y = calculate_points(p1_x, p1_y, 180.0-stone.Angle, offset=-1*offset)
                stone.ROI_Right.Line3[0]    = Point(ps_x, ps_y)
                stone.ROI_Right.Line3[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
                stone.ROI_Right.Line3[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin((stone.Angle + 90.0 )* 3.1415 / 180.0)))
                stone.ROI_Left.Line3[0]     = Point(ps_x, ps_y)
                stone.ROI_Left.Line3[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
                stone.ROI_Left.Line3[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
                

            #
            # draw center line
            #
            cv2.line(cvOutImage, pt1=(stone.ROI_Right.Line2[0].X, stone.ROI_Right.Line2[0].Y), pt2=(stone.ROI_Right.Line2[1].X, stone.ROI_Right.Line2[1].Y), color=(0,255,0), thickness=2)
            cv2.line(cvOutImage, pt1=(stone.ROI_Left.Line2[0].X, stone.ROI_Left.Line2[0].Y), pt2=(stone.ROI_Left.Line2[1].X, stone.ROI_Left.Line2[1].Y), color=(255,0,0), thickness=2)  

            #
            # draw first detection line
            #
            cv2.line(cvOutImage, pt1=(stone.ROI_Right.Line1[0].X, stone.ROI_Right.Line1[0].Y), pt2=(stone.ROI_Right.Line1[1].X, stone.ROI_Right.Line1[1].Y), color=(0,255,255), thickness=2)
            cv2.line(cvOutImage, pt1=(stone.ROI_Left.Line1[0].X, stone.ROI_Left.Line1[0].Y), pt2=(stone.ROI_Left.Line1[1].X, stone.ROI_Left.Line1[1].Y), color=(0,255,255), thickness=2)

            #
            # draw third detection line
            #
            cv2.line(cvOutImage, pt1=(stone.ROI_Right.Line3[0].X, stone.ROI_Right.Line3[0].Y), pt2=(stone.ROI_Right.Line3[1].X, stone.ROI_Right.Line3[1].Y), color=(0,255,255), thickness=2)
            cv2.line(cvOutImage, pt1=(stone.ROI_Left.Line3[0].X, stone.ROI_Left.Line3[0].Y), pt2=(stone.ROI_Left.Line3[1].X, stone.ROI_Left.Line3[1].Y), color=(0,255,255), thickness=2)