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

class StoneProcessing:

    @staticmethod
    def StoneDistances(cvOutImage: np.ndarray, stones: list):
        connected_stones = []
        
        index = 0
        for stone in stones:
            p0 = (np.int32(stone.Center.X), np.int32(stone.Center.Y))
            j = index+1
            while j < len(stones):
                p1 = (np.int32(stones[j].Center.X), np.int32(stones[j].Center.Y))
                d = ( p1[0] - p0[0], p1[1] - p0[1])
                d = np.sqrt( d[0]*d[0] + d[1]*d[1])
                cv2.putText(cvOutImage, str(np.round(d, decimals=2)), org=p0, fontScale=1, color=(0, 255, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX)
                cv2.line(cvOutImage, pt1=p0, pt2=p1, color=(0,255,0), thickness=2)

                if d < 180.0:
                    connected_stones.append([index, j])
                j += 1
            index += 1
        
        #
        #   Calculate Angle between two center lines
        #
        for index_a, index_b in connected_stones:
            
            stone_a = stones[index_a]
            stone_b = stones[index_b]

            b = (stone_a.ROI_Right.Line2[1].X - stone_a.ROI_Right.Line2[0].X, stone_a.ROI_Right.Line2[1].Y - stone_a.ROI_Right.Line2[0].Y)
            d = (stone_b.ROI_Right.Line2[1].X - stone_b.ROI_Right.Line2[0].X, stone_b.ROI_Right.Line2[1].Y - stone_b.ROI_Right.Line2[0].Y)

            v = np.abs(b[0] * d[0] + b[1] * d[1])
            v2 = np.sqrt(b[0]*b[0] + b[1]*b[1]) * np.sqrt(d[0]*d[0] + d[1]*d[1])

            phi = np.arccos(v / v2) * 180.0 / np.pi
            print(phi)

    @staticmethod
    def StoneAngles():
        pass
