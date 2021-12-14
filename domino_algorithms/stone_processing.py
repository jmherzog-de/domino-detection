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

import numpy as np

class StoneProcessing:

    @staticmethod
    def StoneMaches(stones: list):
        """
        Calculate the distance between the left and right center points to other stones.

        :param stones: All DominoStone objects
        :type stones: list
        """
        
        connected_stones = []
        
        #
        # Distance between center of Right and Left sides of a domino stone to another domino stone
        #
        index = 0
        for stone in stones:
            p0_left     = ( np.int32(stone.CenterLeft.X), np.int32(stone.CenterLeft.Y) )
            p0_right    = ( np.int32(stone.CenterRight.X), np.int32(stone.CenterRight.Y) )
            j           = index + 1
            
            while j < len(stones):
                p1_left         = ( np.int32(stones[j].CenterLeft.X), np.int32(stones[j].CenterLeft.Y) )
                p1_right        = ( np.int32(stones[j].CenterRight.X), np.int32(stones[j].CenterRight.Y) )
                
                d_left_left     = p1_left[0] - p0_left[0], p1_left[1] - p0_left[1]
                d_left_left     = np.sqrt( d_left_left[0] * d_left_left[0] + d_left_left[1] * d_left_left[1] )
                
                d_left_right    = p1_right[0] - p0_left[0], p1_right[1] - p0_left[1]
                d_left_right    = np.sqrt( d_left_right[0]*d_left_right[0] + d_left_right[1]*d_left_right[1] )

                d_right_left    = p1_left[0] - p0_right[0], p1_left[1] - p0_right[1]
                d_right_left    = np.sqrt( d_right_left[0]*d_right_left[0] + d_right_left[1]*d_right_left[1])

                d_right_right   = p1_right[0] - p0_right[0], p1_right[1] - p0_right[1]
                d_right_right   = np.sqrt( d_right_right[0]*d_right_right[0] + d_right_right[1]*d_right_right[1])

                
                # calculate shortest distance (only this distance can be the connected stone)
                if d_left_left < 190.0 and d_left_left < d_left_right and d_left_left < d_right_left and d_left_left < d_right_right:
                    connected_stones.append({'a_index': index, 'b_index': j, 'a_side': 'left', 'b_side': 'left'})
                elif d_left_right < 190.0 and d_left_right < d_left_left and d_left_right < d_right_left and d_left_right < d_right_right:
                    connected_stones.append({'a_index': index, 'b_index': j, 'a_side': 'left', 'b_side': 'right'})
                elif d_right_left < 190.0 and d_right_left < d_left_left and d_right_left < d_left_right and d_right_left < d_right_right:
                    connected_stones.append({'a_index': index, 'b_index': j, 'a_side': 'right', 'b_side': 'left'})
                elif d_right_right < 190.0 and d_right_right < d_right_left and d_right_right < d_left_left and d_right_right < d_left_right:
                    connected_stones.append({'a_index': index, 'b_index': j, 'a_side': 'right', 'b_side': 'right'})
                
                j += 1
            index += 1

        #
        # Calculate angle between near stone pairs
        #
        for pair in connected_stones:
            stone_a = stones[pair['a_index']]
            stone_b = stones[pair['b_index']]
            b       = stone_a.ROI_Right.Line2[1].X - stone_a.ROI_Right.Line2[0].X, stone_a.ROI_Right.Line2[1].Y - stone_a.ROI_Right.Line2[0].Y
            d       = stone_b.ROI_Right.Line2[1].X - stone_b.ROI_Right.Line2[0].X, stone_b.ROI_Right.Line2[1].Y - stone_b.ROI_Right.Line2[0].Y
                        
            # calculate the angle between both lines
            v       = np.abs( b[0] * d[0] + b[1] * d[1])
            v2      = np.sqrt( b[0]*b[0] + b[1]*b[1]) * np.sqrt( d[0]*d[0] + d[1]*d[1] )
            phi     = np.arccos(v/v2) * 180.0 / np.pi
            
            if phi >= 85.0 and phi < 91.0 or (phi >= 0.0 and phi <= 5.0):
                val_a = stone_a.EyeVal_Left if pair['a_side'] == 'left' else stone_a.EyeVal_Right
                val_b = stone_b.EyeVal_Right if pair['b_side'] == 'left' else stone_b.EyeVal_Right
                stones[pair['a_index']].Connected_Stones.append({'index': pair['b_index'], 'valid': val_a == val_b})
                stones[pair['b_index']].Connected_Stones.append({'index': pair['a_index'], 'valid': val_a == val_b})
        
        return