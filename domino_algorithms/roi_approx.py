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
from domino_algorithms.domino_stone import ROI, DominoStone, Point


def calculate_points(center_x: int, center_y: int, angle: float, offset: float):
    """
    Calculate new point with offset on line with given center coordinates and angle.

    :param center_x: Center point x-coordinate.
    :type center_x: int
    :param center_y: Center point y-coordinate.
    :type center_y: int
    :param angle: Angle in degree
    :type angle: float
    :param offset: offset between center and point
    :type offset: float
    :return: (x-coordinate, y-coordiante)
    :rtype: (int32, int32)
    """
    
    sin     = np.sin(angle * 3.1415 / 180.0)
    cos     = np.cos(angle * 3.1415 / 180.0)

    # angle tolerance of 5 degrees. Angles lower
    # 5 deg will be interpreted as vertical lines
    if angle > 5.0:
        ps_y = center_y - offset * sin
        ps_x = center_x + offset * cos
    else:
        ps_y = center_y + offset
        ps_x = center_x
    
    return np.int32(np.round(ps_x)), np.int32(np.round(ps_y))

class RoiApprox:

    @staticmethod
    def Calculate_Stone_Edges_90_DEG(stone: DominoStone, divider_center_y: np.int32, stone_length: np.int32):
        
        if stone.Width < stone.Height:

            stone.StoneEdges[0].X = stone.CenterLine_P1.X
            stone.StoneEdges[0].Y = np.int32(stone.CenterLine_P1.Y + stone_length * 0.5)

            stone.StoneEdges[1].X = stone.CenterLine_P1.X
            stone.StoneEdges[1].Y = np.int32(divider_center_y - stone_length * 0.5)

            stone.StoneEdges[2].X = stone.CenterLine_P2.X
            stone.StoneEdges[2].Y = np.int32(stone.CenterLine_P2.Y + stone_length * 0.5)

            stone.StoneEdges[3].X = stone.CenterLine_P2.X
            stone.StoneEdges[3].Y = np.int32(stone.CenterLine_P2.Y - stone_length * 0.5) 
        else:

            stone.StoneEdges[0].X = np.int32(stone.CenterLine_P1.X + stone_length * 0.5)
            stone.StoneEdges[0].Y = stone.CenterLine_P1.Y

            stone.StoneEdges[1].X   = np.int32(stone.CenterLine_P1.X - stone_length * 0.5)
            stone.StoneEdges[1].Y   = stone.CenterLine_P1.Y

            stone.StoneEdges[2].X   = np.int32(stone.CenterLine_P2.X + stone_length * 0.5)
            stone.StoneEdges[2].Y   = stone.CenterLine_P2.Y

            stone.StoneEdges[3].X   = np.int32(stone.CenterLine_P2.X - stone_length * 0.5)
            stone.StoneEdges[3].Y   = stone.CenterLine_P2.Y

    @staticmethod
    def Calculate_Detection_Row_One_90_DEG(stone: DominoStone, divider_center_x: np.int32, divider_center_y: np.int32, offset: np.int32, stone_length: np.int32):

        if stone.Width < stone.Height:
            # Calculate start and end-point of the detection row on the right side
            stone.ROI_Right.Line1[0].X = divider_center_x - offset
            stone.ROI_Right.Line1[0].Y = divider_center_y
            stone.ROI_Right.Line1[1].X = divider_center_x - offset
            stone.ROI_Right.Line1[1].Y = np.int32(divider_center_y + stone_length * 0.5)

            # Calculate start and end-point of the detection row on the left side
            stone.ROI_Left.Line1[0].X = divider_center_x - offset
            stone.ROI_Left.Line1[0].Y = divider_center_y
            stone.ROI_Left.Line1[1].X = divider_center_x - offset
            stone.ROI_Left.Line1[1].Y = np.int32(divider_center_y - stone_length * 0.5)

            # Possible Eye center positions on the right side
            stone.ROI_Right.Line1_Points[0].X    = divider_center_x - offset
            stone.ROI_Right.Line1_Points[0].Y    = np.int32(divider_center_y + 25)
            stone.ROI_Right.Line1_Points[1].X    = divider_center_x - offset
            stone.ROI_Right.Line1_Points[1].Y    = np.int32(divider_center_y + 55)
            stone.ROI_Right.Line1_Points[2].X    = divider_center_x - offset
            stone.ROI_Right.Line1_Points[2].Y    = np.int32(divider_center_y + 85)

            # Possible Eye center positions on the left side
            stone.ROI_Left.Line1_Points[0].X    = divider_center_x - offset
            stone.ROI_Left.Line1_Points[0].Y    = np.int32(divider_center_y - 25)
            stone.ROI_Left.Line1_Points[1].X    = divider_center_x - offset
            stone.ROI_Left.Line1_Points[1].Y    = np.int32(divider_center_y - 55)
            stone.ROI_Left.Line1_Points[2].X    = divider_center_x - offset
            stone.ROI_Left.Line1_Points[2].Y    = np.int32(divider_center_y - 85)
        else:
            # Calculate start and end-point of the detection row on the right side
            stone.ROI_Right.Line1[0].X = divider_center_x
            stone.ROI_Right.Line1[0].Y = divider_center_y + offset
            stone.ROI_Right.Line1[1].X = np.int32(divider_center_x + stone_length * 0.5)
            stone.ROI_Right.Line1[1].Y = divider_center_y + offset

            # Calculate start and end-point of the detection row on the left side
            stone.ROI_Left.Line1[0].X = divider_center_x
            stone.ROI_Left.Line1[0].Y = divider_center_y + offset
            stone.ROI_Left.Line1[1].X = np.int32(divider_center_x - stone_length * 0.5)
            stone.ROI_Left.Line1[1].Y = divider_center_y + offset

            # Possible Eye center positions on the right side
            stone.ROI_Right.Line1_Points[0].X   = np.int32(divider_center_x + 25)
            stone.ROI_Right.Line1_Points[0].Y   = divider_center_y + offset
            stone.ROI_Right.Line1_Points[1].X   = np.int32(divider_center_x + 55)
            stone.ROI_Right.Line1_Points[1].Y   = divider_center_y + offset
            stone.ROI_Right.Line1_Points[2].X   = np.int32(divider_center_x + 85)
            stone.ROI_Right.Line1_Points[2].Y   = divider_center_y + offset

            # Possible Eye center positions on the left side
            stone.ROI_Left.Line1_Points[0].X   = np.int32(divider_center_x - 25)
            stone.ROI_Left.Line1_Points[0].Y   = divider_center_y + offset
            stone.ROI_Left.Line1_Points[1].X   = np.int32(divider_center_x - 55)
            stone.ROI_Left.Line1_Points[1].Y   = divider_center_y + offset
            stone.ROI_Left.Line1_Points[2].X   = np.int32(divider_center_x - 85)
            stone.ROI_Left.Line1_Points[2].Y   = divider_center_y + offset
            
    @staticmethod
    def Calculate_Detection_Row_Two_90_DEG(stone: DominoStone, divider_center_x: np.int32, divider_center_y: np.int32, offset: np.int32, stone_length: np.int32):
        
        stone.ROI_Right.Line2[0]    = Point(divider_center_x, divider_center_y)
        stone.ROI_Left.Line2[0]     = Point(divider_center_x, divider_center_y)

        if stone.Width < stone.Height:

            # Calculate start and end-point of the detection row on the right side
            stone.ROI_Right.Line2[1].X  = divider_center_x
            stone.ROI_Right.Line2[1].Y  = np.int32(np.round(stone.Center.Y + stone_length * 0.5))

            # Calculate the start and end-point of the detection row on the left side
            stone.ROI_Left.Line2[1].X   = divider_center_x
            stone.ROI_Left.Line2[1].Y   = np.int32(np.round(stone.Center.Y - stone_length * 0.5))

            # Possible Eye center positions on the right side
            stone.ROI_Right.Line2_Points[0].X   = divider_center_x
            stone.ROI_Right.Line2_Points[0].Y   = np.int32(divider_center_y + 55)

            # Possible Eye center positions on the left side
            stone.ROI_Left.Line2_Points[0].X    = divider_center_x
            stone.ROI_Left.Line2_Points[0].Y    = np.int32(divider_center_y - 55)

            # Calculate right center point of the domino stone
            stone.CenterRight.X         = divider_center_x
            stone.CenterRight.Y         = np.int32(np.round(stone.Center.Y + stone_length * 0.25))

            # Calculate left center point of the domino stone
            stone.CenterLeft.X          = divider_center_x
            stone.CenterLeft.Y          = np.int32(np.round(stone.Center.Y - stone_length * 0.25))

        else:

            # Calculate start and end-point of the detection row on the right side
            stone.ROI_Right.Line2[1].X  = np.int32(np.round(stone.Center.X + stone_length * 0.5))
            stone.ROI_Right.Line2[1].Y  = divider_center_y

            # Calculate start and end-point of the detection row on the left side
            stone.ROI_Left.Line2[1].X   = np.int32(np.round(stone.Center.X - stone_length * 0.5))
            stone.ROI_Left.Line2[1].Y   = divider_center_y

            # Possible Eye center positions on the right side
            stone.ROI_Right.Line2_Points[0].X   = divider_center_x + 55
            stone.ROI_Right.Line2_Points[0].Y    = divider_center_y

            # Possible Eye center position on the left side
            stone.ROI_Left.Line2_Points[0].X    = divider_center_x - 55
            stone.ROI_Left.Line2_Points[0].Y    = divider_center_y

            # Calculate right center point of the domino stone
            stone.CenterRight.X = np.int32(np.round(divider_center_x + stone_length * 0.25))
            stone.CenterRight.Y = divider_center_y

            # Calculate left center point of the domino stone
            stone.CenterLeft.X  = np.int32(np.round(divider_center_x - stone_length * 0.25))
            stone.CenterLeft.Y  = divider_center_y

    @staticmethod
    def Calculate_Detection_Row_Three_90_DEG(stone: DominoStone, divider_center_x: np.int32, divider_center_y: np.int32, offset: np.int32, stone_length: np.int32):
        
        if stone.Width < stone.Height:
            
            # Possible Eye center position on the right side
            stone.ROI_Right.Line3_Points[0].X   = divider_center_x + offset
            stone.ROI_Right.Line3_Points[0].Y   = np.int32(divider_center_y + 25)
            stone.ROI_Right.Line3_Points[1].X   = divider_center_x + offset
            stone.ROI_Right.Line3_Points[1].Y   = np.int32(divider_center_y + 55)
            stone.ROI_Right.Line3_Points[2].X   = divider_center_x + offset
            stone.ROI_Right.Line3_Points[2].Y   = np.int32(divider_center_y + 85)

            # Possible Eye center position on the left side
            stone.ROI_Left.Line3_Points[0].X   = divider_center_x + offset
            stone.ROI_Left.Line3_Points[0].Y   = np.int32(divider_center_y - 25)
            stone.ROI_Left.Line3_Points[1].X   = divider_center_x + offset
            stone.ROI_Left.Line3_Points[1].Y   = np.int32(divider_center_y - 55)
            stone.ROI_Left.Line3_Points[2].X   = divider_center_x + offset
            stone.ROI_Left.Line3_Points[2].Y   = np.int32(divider_center_y - 85)

            # Calculate start and end-point of the detection row on the right side
            stone.ROI_Right.Line3[0].X = divider_center_x + offset
            stone.ROI_Right.Line3[0].Y = divider_center_y
            stone.ROI_Right.Line3[1].X = divider_center_x + offset
            stone.ROI_Right.Line3[1].Y = np.int32(divider_center_y + stone_length * 0.5)

            # Calculate start and end-point of the detection row on the left side
            stone.ROI_Left.Line3[0].X = divider_center_x + offset
            stone.ROI_Left.Line3[0].Y = divider_center_y
            stone.ROI_Left.Line3[1].X = divider_center_x + offset
            stone.ROI_Left.Line3[1].Y = np.int32(divider_center_y - stone_length * 0.5)

        else:

            # Calculate start and end-point of the detection row on the right side
            stone.ROI_Right.Line3[0].X = divider_center_x
            stone.ROI_Right.Line3[0].Y = divider_center_y - offset
            stone.ROI_Right.Line3[1].X = np.int32(divider_center_x + stone_length * 0.5)
            stone.ROI_Right.Line3[1].Y = divider_center_y - offset

            # Calculate start and end-point of the detection row on the left side
            stone.ROI_Left.Line3[0].X = divider_center_x
            stone.ROI_Left.Line3[0].Y = divider_center_y - offset
            stone.ROI_Left.Line3[1].X = np.int32(divider_center_x - stone_length * 0.5)
            stone.ROI_Left.Line3[1].Y = divider_center_y - offset

            # Possible eye center positions on the right side
            stone.ROI_Right.Line3_Points[0].X   = np.int32(divider_center_x + 25)
            stone.ROI_Right.Line3_Points[0].Y   = divider_center_y - offset
            stone.ROI_Right.Line3_Points[1].X   = np.int32(divider_center_x + 55)
            stone.ROI_Right.Line3_Points[1].Y   = divider_center_y - offset
            stone.ROI_Right.Line3_Points[2].X   = np.int32(divider_center_x + 85)
            stone.ROI_Right.Line3_Points[2].Y   = divider_center_y - offset

            # Possible eye center positions on the left side
            stone.ROI_Left.Line3_Points[0].X    = np.int32(divider_center_x - 25)
            stone.ROI_Left.Line3_Points[0].Y    = divider_center_y - offset
            stone.ROI_Left.Line3_Points[1].X    = np.int32(divider_center_x - 55)
            stone.ROI_Left.Line3_Points[1].Y    = divider_center_y - offset
            stone.ROI_Left.Line3_Points[2].X    = np.int32(divider_center_x - 85)
            stone.ROI_Left.Line3_Points[2].Y    = divider_center_y - offset


    @staticmethod
    def Calculate_Stone_Edges(stone: DominoStone, stone_length: np.int32):
        
        if stone.Height > stone.Width:
            stone.StoneEdges[0].X       = np.int32(np.round(stone.CenterLine_P1.X + stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[0].Y       = np.int32(np.round(stone.CenterLine_P1.Y + stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[1].X       = np.int32(np.round(stone.CenterLine_P1.X - stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[1].Y       = np.int32(np.round(stone.CenterLine_P1.Y - stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[2].X       = np.int32(np.round(stone.CenterLine_P2.X + stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[2].Y       = np.int32(np.round(stone.CenterLine_P2.Y + stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[3].X       = np.int32(np.round(stone.CenterLine_P2.X - stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.StoneEdges[3].Y       = np.int32(np.round(stone.CenterLine_P2.Y - stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))
        else:
            stone.StoneEdges[0].X       = np.int32(np.round(stone.CenterLine_P1.X + stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.StoneEdges[0].Y       = np.int32(np.round(stone.CenterLine_P1.Y + stone_length * 0.5 * np.sin((stone.Angle + 90.0 )* 3.1415 / 180.0)))
            stone.StoneEdges[1].X       = np.int32(np.round(stone.CenterLine_P1.X - stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.StoneEdges[1].Y       = np.int32(np.round(stone.CenterLine_P1.Y - stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.StoneEdges[2].X       = np.int32(np.round(stone.CenterLine_P2.X + stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.StoneEdges[2].Y       = np.int32(np.round(stone.CenterLine_P2.Y + stone_length * 0.5 * np.sin((stone.Angle + 90.0 )* 3.1415 / 180.0)))
            stone.StoneEdges[3].X       = np.int32(np.round(stone.CenterLine_P2.X - stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.StoneEdges[3].Y       = np.int32(np.round(stone.CenterLine_P2.Y - stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

    @staticmethod
    def Calculate_Detection_Row_One(stone: DominoStone, divider_center_x: np.int32, divider_center_y: np.int32, offset: np.int32, stone_length: np.int32):
        
        if stone.Height > stone.Width:
            
            # Calculate start and end-point of detection row on the right side
            ps_x, ps_y = calculate_points(divider_center_x, divider_center_y, 90.0 - stone.Angle, offset)
            stone.ROI_Right.Line1[0]    = Point(ps_x, ps_y)
            stone.ROI_Right.Line1[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line1[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))

            # Calculate start and end-point of detection row on the left side
            stone.ROI_Left.Line1[0]     = Point(ps_x, ps_y)
            stone.ROI_Left.Line1[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line1[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))

            # Possible Eye center position on the right side
            stone.ROI_Right.Line1_Points[0].X   = np.int32(np.round(ps_x + 25 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[0].Y   = np.int32(np.round(ps_y + 25 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[1].X   = np.int32(np.round(ps_x + 55 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[1].Y   = np.int32(np.round(ps_y + 55 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[2].X   = np.int32(np.round(ps_x + 85 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[2].Y   = np.int32(np.round(ps_y + 85 * np.sin(stone.Angle * 3.1415 / 180.0)))

            # Possible Eye center position on the left side
            stone.ROI_Left.Line1_Points[0].X   = np.int32(np.round(ps_x - 25 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[0].Y   = np.int32(np.round(ps_y - 25 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[1].X   = np.int32(np.round(ps_x - 55 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[1].Y   = np.int32(np.round(ps_y - 55 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[2].X   = np.int32(np.round(ps_x - 85 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[2].Y   = np.int32(np.round(ps_y - 85 * np.sin(stone.Angle * 3.1415 / 180.0)))

        else:

            # Calculate start and end-point of detection row on the right side
            ps_x, ps_y = calculate_points(divider_center_x, divider_center_y, 180.0 - stone.Angle, offset)
            stone.ROI_Right.Line1[0]    = Point(ps_x, ps_y)
            stone.ROI_Right.Line1[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line1[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

            # Calculate start and end-point of detection row on the left side
            stone.ROI_Left.Line1[0]     = Point(ps_x, ps_y)
            stone.ROI_Left.Line1[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line1[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

            # Possible Eye center position on the right side
            stone.ROI_Right.Line1_Points[0].X   = np.int32(np.round(ps_x + 25 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[0].Y   = np.int32(np.round(ps_y + 25 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[1].X   = np.int32(np.round(ps_x + 55 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[1].Y   = np.int32(np.round(ps_y + 55 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[2].X   = np.int32(np.round(ps_x + 85 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line1_Points[2].Y   = np.int32(np.round(ps_y + 85 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

            # Possible Eye center position on the left side
            stone.ROI_Left.Line1_Points[0].X   = np.int32(np.round(ps_x - 25 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[0].Y   = np.int32(np.round(ps_y - 25 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[1].X   = np.int32(np.round(ps_x - 55 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[1].Y   = np.int32(np.round(ps_y - 55 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[2].X   = np.int32(np.round(ps_x - 85 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line1_Points[2].Y   = np.int32(np.round(ps_y - 85 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
    
    @staticmethod
    def Calculate_Detection_Row_Two(stone: DominoStone, divider_center_x: np.int32, divider_center_y: np.int32, offset: np.int32, stone_length: np.int32):
        
        stone.ROI_Right.Line2[0]    = Point(divider_center_x, divider_center_y)
        stone.ROI_Left.Line2[0]     = Point(divider_center_x, divider_center_y)

        if stone.Height > stone.Width:
            
            # Calculate start and end-point of detection row on the right side
            stone.ROI_Right.Line2[0]    = Point(divider_center_x, divider_center_y)
            stone.ROI_Right.Line2[1].X  = np.int32(np.round(stone.Center.X + stone_length * 0.5 * np.cos((stone.Angle) * 3.1415 / 180.0)))
            stone.ROI_Right.Line2[1].Y  = np.int32(np.round(stone.Center.Y + stone_length * 0.5 * np.sin((stone.Angle) * 3.1415 / 180.0)))

            # Calculate start and end-point of detection row on the left side
            stone.ROI_Left.Line2[0]     = Point(divider_center_x, divider_center_y)
            stone.ROI_Left.Line2[1].X   = np.int32(np.round(stone.Center.X - stone_length * 0.5 * np.cos((stone.Angle) * 3.1415 / 180.0)))
            stone.ROI_Left.Line2[1].Y   = np.int32(np.round(stone.Center.Y - stone_length * 0.5 * np.sin((stone.Angle) * 3.1415 / 180.0)))

            # Calculate right center point of the domino stone
            stone.CenterRight.X         = np.int32(np.round(stone.Center.X + stone_length * 0.25 * np.cos((stone.Angle) * 3.1415 / 180.0)))
            stone.CenterRight.Y         = np.int32(np.round(stone.Center.Y + stone_length * 0.25 * np.sin((stone.Angle) * 3.1415 / 180.0)))

            # Calculate left center point of the domino stone
            stone.CenterLeft.X          = np.int32(np.round(stone.Center.X - stone_length * 0.25 * np.cos((stone.Angle) * 3.1415 / 180.0)))
            stone.CenterLeft.Y          = np.int32(np.round(stone.Center.Y - stone_length * 0.25 * np.sin((stone.Angle) * 3.1415 / 180.0)))

            # Possible Eye center position on the right side
            stone.ROI_Right.Line2_Points[0].X   = np.int32(np.round(stone.Center.X + 55 * np.cos((stone.Angle) * 3.1415 / 180.0)))
            stone.ROI_Right.Line2_Points[0].Y   = np.int32(np.round(stone.Center.Y + 55 * np.sin((stone.Angle) * 3.1415 / 180.0)))

            # Possible Eye center position on the left side
            stone.ROI_Left.Line2_Points[0].X   = np.int32(np.round(stone.Center.X - 55 * np.cos((stone.Angle) * 3.1415 / 180.0)))
            stone.ROI_Left.Line2_Points[0].Y   = np.int32(np.round(stone.Center.Y - 55 * np.sin((stone.Angle) * 3.1415 / 180.0)))

        else:
            
            # Calculate start and end-point of detection row on the right side
            calc_angle = stone.Angle + 90.0
            stone.ROI_Right.Line2[1].X  = np.int32(np.round(stone.Center.X + stone_length * 0.5 * np.cos((calc_angle) * 3.1415 / 180.0)))
            stone.ROI_Right.Line2[1].Y  = np.int32(np.round(stone.Center.Y + stone_length * 0.5 * np.sin((calc_angle) * 3.1415 / 180.0)))

            # Calculate start and end-point of detection row on the left side
            stone.ROI_Left.Line2[1].X   = np.int32(np.round(stone.Center.X - stone_length * 0.5 * np.cos((calc_angle) * 3.1415 / 180.0)))
            stone.ROI_Left.Line2[1].Y   = np.int32(np.round(stone.Center.Y - stone_length * 0.5 * np.sin((calc_angle) * 3.1415 / 180.0)))

            # Calculate right center point of the domino stone
            stone.CenterRight.X         = np.int32(np.round(stone.Center.X + stone_length * 0.25 * np.cos((calc_angle) * 3.1415 / 180.0)))
            stone.CenterRight.Y         = np.int32(np.round(stone.Center.Y + stone_length * 0.25 * np.sin((calc_angle) * 3.1415 / 180.0)))

            # Calculate left center point of the domino stone
            stone.CenterLeft.X          = np.int32(np.round(stone.Center.X - stone_length * 0.25 * np.cos((calc_angle) * 3.1415 / 180.0)))
            stone.CenterLeft.Y          = np.int32(np.round(stone.Center.Y - stone_length * 0.25 * np.sin((calc_angle) * 3.1415 / 180.0)))

            # Possible Eye center position on the right side
            stone.ROI_Right.Line2_Points[0].X   = np.int32(np.round(stone.Center.X + 55 * np.cos((calc_angle) * 3.1415 / 180.0)))
            stone.ROI_Right.Line2_Points[0].Y   = np.int32(np.round(stone.Center.Y + 55 * np.sin((calc_angle) * 3.1415 / 180.0)))

            # Possible Eye center position on rhe left side
            stone.ROI_Left.Line2_Points[0].X    = np.int32(np.round(stone.Center.X - 55 * np.cos((calc_angle) * 3.1415 / 180.0)))
            stone.ROI_Left.Line2_Points[0].Y    = np.int32(np.round(stone.Center.Y - 55 * np.sin((calc_angle) * 3.1415 / 180.0)))

    @staticmethod
    def Calculate_Detection_Row_Three(stone: DominoStone, divider_center_x: np.int32, divider_center_y: np.int32, offset: np.int32, stone_length: np.int32):
        
        if stone.Height > stone.Width:

            # Calculate start and end-point of detection row on the right side
            ps_x, ps_y                  = calculate_points(divider_center_x, divider_center_y, 90.0-stone.Angle, offset=-1*offset)
            stone.ROI_Right.Line3[0]    = Point(ps_x, ps_y)
            stone.ROI_Right.Line3[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line3[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))

            # Calculate start and end-point of detection row on the left side
            stone.ROI_Left.Line3[0]     = Point(ps_x, ps_y)
            stone.ROI_Left.Line3[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line3[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin(stone.Angle * 3.1415 / 180.0)))

            # Possible Eye center point on the right side
            stone.ROI_Right.Line3_Points[0].X   = np.int32(np.round(ps_x + 25 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[0].Y   = np.int32(np.round(ps_y + 25 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[1].X   = np.int32(np.round(ps_x + 55 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[1].Y   = np.int32(np.round(ps_y + 55 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[2].X   = np.int32(np.round(ps_x + 85 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[2].Y   = np.int32(np.round(ps_y + 85 * np.sin(stone.Angle * 3.1415 / 180.0)))

            # Possible Eye center point on the left side
            stone.ROI_Left.Line3_Points[0].X   = np.int32(np.round(ps_x - 25 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[0].Y   = np.int32(np.round(ps_y - 25 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[1].X   = np.int32(np.round(ps_x - 55 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[1].Y   = np.int32(np.round(ps_y - 55 * np.sin(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[2].X   = np.int32(np.round(ps_x - 85 * np.cos(stone.Angle * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[2].Y   = np.int32(np.round(ps_y - 85 * np.sin(stone.Angle * 3.1415 / 180.0)))
        
        else:
            # Calculate start and end-point of detection row on the right side
            ps_x, ps_y = calculate_points(divider_center_x, divider_center_y, 180.0-stone.Angle, offset=-1*offset)
            stone.ROI_Right.Line3[0]    = Point(ps_x, ps_y)
            stone.ROI_Right.Line3[1].X  = np.int32(np.round(ps_x + stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line3[1].Y  = np.int32(np.round(ps_y + stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

            # Calculate start and end-point of detection row on the left side
            stone.ROI_Left.Line3[0]     = Point(ps_x, ps_y)
            stone.ROI_Left.Line3[1].X   = np.int32(np.round(ps_x - stone_length * 0.5 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line3[1].Y   = np.int32(np.round(ps_y - stone_length * 0.5 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

            # Possible Eye center point on the right side
            stone.ROI_Right.Line3_Points[0].X   = np.int32(np.round(ps_x + 25 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[0].Y   = np.int32(np.round(ps_y + 25 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[1].X   = np.int32(np.round(ps_x + 55 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[1].Y   = np.int32(np.round(ps_y + 55 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[2].X   = np.int32(np.round(ps_x + 85 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Right.Line3_Points[2].Y   = np.int32(np.round(ps_y + 85 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))

            # Possible Eye center point on the left side
            stone.ROI_Left.Line3_Points[0].X   = np.int32(np.round(ps_x - 25 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[0].Y   = np.int32(np.round(ps_y - 25 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[1].X   = np.int32(np.round(ps_x - 55 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[1].Y   = np.int32(np.round(ps_y - 55 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[2].X   = np.int32(np.round(ps_x - 85 * np.cos((stone.Angle + 90.0) * 3.1415 / 180.0)))
            stone.ROI_Left.Line3_Points[2].Y   = np.int32(np.round(ps_y - 85 * np.sin((stone.Angle + 90.0) * 3.1415 / 180.0)))



    @staticmethod
    def Draw(stone: DominoStone, image: np.ndarray):
        # draw center line
        cv2.line(image, pt1=(stone.ROI_Right.Line2[0].X, stone.ROI_Right.Line2[0].Y), pt2=(stone.ROI_Right.Line2[1].X, stone.ROI_Right.Line2[1].Y), color=(0,255,0), thickness=2)
        cv2.line(image, pt1=(stone.ROI_Left.Line2[0].X, stone.ROI_Left.Line2[0].Y), pt2=(stone.ROI_Left.Line2[1].X, stone.ROI_Left.Line2[1].Y), color=(255,0,0), thickness=2)  

        # draw first detection line
        cv2.line(image, pt1=(stone.ROI_Right.Line1[0].X, stone.ROI_Right.Line1[0].Y), pt2=(stone.ROI_Right.Line1[1].X, stone.ROI_Right.Line1[1].Y), color=(0,255,255), thickness=2)
        cv2.line(image, pt1=(stone.ROI_Left.Line1[0].X, stone.ROI_Left.Line1[0].Y), pt2=(stone.ROI_Left.Line1[1].X, stone.ROI_Left.Line1[1].Y), color=(0,255,255), thickness=2)

        # draw third detection line
        cv2.line(image, pt1=(stone.ROI_Right.Line3[0].X, stone.ROI_Right.Line3[0].Y), pt2=(stone.ROI_Right.Line3[1].X, stone.ROI_Right.Line3[1].Y), color=(0,255,255), thickness=2)
        cv2.line(image, pt1=(stone.ROI_Left.Line3[0].X, stone.ROI_Left.Line3[0].Y), pt2=(stone.ROI_Left.Line3[1].X, stone.ROI_Left.Line3[1].Y), color=(0,255,255), thickness=2)

        #draw points of detection row 1 right side
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line1_Points[0].X), np.int32(stone.ROI_Right.Line1_Points[0].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line1_Points[1].X), np.int32(stone.ROI_Right.Line1_Points[1].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line1_Points[2].X), np.int32(stone.ROI_Right.Line1_Points[2].Y)), radius=10, color=(0,0,255), thickness=2)

        # draw points of detection row 2 right side
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line2_Points[0].X), np.int32(stone.ROI_Right.Line2_Points[0].Y)), radius=10, color=(0,0,255), thickness=2)
        
        # draw points of detection row 3 right side
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line3_Points[0].X), np.int32(stone.ROI_Right.Line3_Points[0].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line3_Points[1].X), np.int32(stone.ROI_Right.Line3_Points[1].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Right.Line3_Points[2].X), np.int32(stone.ROI_Right.Line3_Points[2].Y)), radius=10, color=(0,0,255), thickness=2)

        # draw points of detection row 1 left side
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line1_Points[0].X), np.int32(stone.ROI_Left.Line1_Points[0].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line1_Points[1].X), np.int32(stone.ROI_Left.Line1_Points[1].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line1_Points[2].X), np.int32(stone.ROI_Left.Line1_Points[2].Y)), radius=10, color=(0,0,255), thickness=2)

        # draw points of detection row 2 left side
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line2_Points[0].X), np.int32(stone.ROI_Left.Line2_Points[0].Y)), radius=10, color=(0,0,255), thickness=2)

        # draw points of detection row 3 left side
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line3_Points[0].X), np.int32(stone.ROI_Left.Line3_Points[0].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line3_Points[1].X), np.int32(stone.ROI_Left.Line3_Points[1].Y)), radius=10, color=(0,0,255), thickness=2)
        cv2.circle(image, center=(np.int32(stone.ROI_Left.Line3_Points[2].X), np.int32(stone.ROI_Left.Line3_Points[2].Y)), radius=10, color=(0,0,255), thickness=2)

        # Draw stone edges
        cv2.circle(image, center=(np.int32(stone.StoneEdges[0].X), np.int32(stone.StoneEdges[0].Y)), radius=3, color=(0,0,255), thickness=3)
        cv2.circle(image, center=(np.int32(stone.StoneEdges[1].X), np.int32(stone.StoneEdges[1].Y)), radius=3, color=(0,0,255), thickness=3)
        cv2.circle(image, center=(np.int32(stone.StoneEdges[2].X), np.int32(stone.StoneEdges[2].Y)), radius=3, color=(0,0,255), thickness=3)
        cv2.circle(image, center=(np.int32(stone.StoneEdges[3].X), np.int32(stone.StoneEdges[3].Y)), radius=3, color=(0,0,255), thickness=3)


    @staticmethod
    def FindROI(stones: list, cvOutImage: np.ndarray, stone_length: int = 200, offset: int = 30):
        """
        Extract Region Of Interest lines for all domino-stones.
        Each stone has three detection lines for right and left handside.

        :param stones: DominoStone objects found.
        :type stones: list
        :param cvOutImage: OpenCV Output image. Will be filled with the ROI lines.
        :type cvOutImage: np.ndarray
        :param stone_length: domino-stone total length in pixel, defaults to 200
        :type stone_length: int, optional
        :param offset: Offset between the detection rows on the center line, defaults to 30
        :type offset: int, optional
        """
        
        for stone in stones:

            # Extract divider center points and convert them into decimals
            # Note: this is needed to draw the center line.
            p1_x = np.int32(np.round(stone.Center.X))
            p1_y = np.int32(np.round(stone.Center.Y))

            #print(stone.Angle)
                        
            if stone.Angle >= 85.0 and stone.Angle <= 91.0:
                RoiApprox.Calculate_Stone_Edges_90_DEG(stone, divider_center_y=p1_y, stone_length=stone_length)
                RoiApprox.Calculate_Detection_Row_One_90_DEG(stone, divider_center_x=p1_x, divider_center_y=p1_y, offset=offset, stone_length=stone_length)
                RoiApprox.Calculate_Detection_Row_Two_90_DEG(stone, divider_center_x=p1_x, divider_center_y=p1_y, offset=offset, stone_length=stone_length)
                RoiApprox.Calculate_Detection_Row_Three_90_DEG(stone, divider_center_x=p1_x, divider_center_y=p1_y, offset=offset, stone_length=stone_length)         
            else:
                RoiApprox.Calculate_Stone_Edges(stone, stone_length)
                RoiApprox.Calculate_Detection_Row_One(stone, divider_center_x=p1_x, divider_center_y=p1_y, offset=offset, stone_length=stone_length)
                RoiApprox.Calculate_Detection_Row_Two(stone, divider_center_x=p1_x, divider_center_y=p1_y, offset=offset, stone_length=stone_length)
                RoiApprox.Calculate_Detection_Row_Three(stone, divider_center_x=p1_x, divider_center_y=p1_y, offset=offset, stone_length=stone_length)                

            RoiApprox.Draw(stone, cvOutImage)