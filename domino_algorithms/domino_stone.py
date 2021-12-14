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

class Point:

    def __init__(self, x: float, y: float) -> None:
        self.X = x
        self.Y = y

class ROI:

    def __init__(self) -> None:
        self.Line1  = [ Point(0.0, 0.0), Point(0.0, 0.0) ]
        self.Line2  = [ Point(0.0, 0.0), Point(0.0, 0.0) ]
        self.Line3  = [ Point(0.0, 0.0), Point(0.0, 0.0) ]

class DominoStone:

    def __init__(self, center_x: float = 0.0, center_y: float = 0.0, length: float = 0.0, width: float = 0.0, height: float = 0.0, angle_deg: float = 0.0, center_line_p1_x: float = 0.0, center_line_p1_y: float = 0.0, center_line_p2_x: float = 0.0, center_line_p2_y: float = 0.0) -> None:
        
        # Center Point coordinates of the domino stone
        self.Center         = Point(center_x, center_y)

        # First Point of the stone center line.
        self.CenterLine_P1  = Point(center_line_p1_x, center_line_p1_y)

        # Second Point of the stone center line.
        self.CenterLine_P2  = Point(center_line_p2_x, center_line_p2_y)

        # Center Point coordinates of the right side (ROI).
        self.CenterRight    = Point(0.0, 0.0)

        # Center Point coordinates of the left side (ROI).
        self.CenterLeft     = Point(0.0, 0.0)

        # Approximated Stone edges.
        self.StoneEdges     = [Point(0.0, 0.0), Point(0.0, 0.0), Point(0.0, 0.0), Point(0.0, 0.0)]

        # Divider line length of the domino stone.
        self.Length         = length

        # Divider line height.
        self.Height         = height

        # Divider line width.
        self.Width          = width

        # approximated angle of the domino stone.
        self.Angle          = angle_deg

        # Region of interest points at the left side of the domino stone.
        self.ROI_Left       = ROI()

        # Region of interest points at the right side of the domino stone.
        self.ROI_Right      = ROI()

        # Points detected on the left side.
        self.Eyes_Left      = list()

        # Points detected on the right side.
        self.Eyes_Right     = list()

        # Eye Value of the right side.
        self.EyeVal_Right   = 0

        # Eye value of the left side.
        self.EyeVal_Left    = 0

        # Contains all indexes of the connected stones.
        self.Connected_Stones = []