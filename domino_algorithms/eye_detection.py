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

from math import e
import cv2
import numpy as np

from domino_algorithms.domino_stone import Point

class DominoEyeDetection:

    @staticmethod
    def ExtractEyes(cvImage: np.ndarray, cvOutImage: np.ndarray, min_dist: int, param_1: int, param_2: int, min_radius: int, max_radius: int, eyes_list: list):
        """
        Detect circles in the given input image and add them into the eyes_list.

        :param cvImage: OpenCV input image.
        :type cvImage: np.ndarray
        :param cvOutImage: OpenCV Output image with all found circles.
        :type cvOutImage: np.ndarray
        :param min_dist: Minimum distance between circles
        :type min_dist: int
        :param param_1: [description]
        :type param_1: int
        :param param_2: [description]
        :type param_2: int
        :param min_radius: Minimum radius of circles to detect.
        :type min_radius: int
        :param max_radius: Maximum radius of circles to detect.
        :type max_radius: int
        :param eyes_list: List to write all found circles {X, Y, Radius}
        :type eyes_list: list
        """

        eyes_list.clear()

        detected_circles = cv2.HoughCircles(cvImage, method=cv2.HOUGH_GRADIENT, dp=1, minDist=min_dist, param1=param_1, param2=param_2, minRadius=min_radius, maxRadius=max_radius)

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                center_x, center_y, r = pt[0], pt[1], pt[2]
                eyes_list.append({'X': center_x, 'Y': center_y, 'Radius': r})
                cv2.circle(cvOutImage, (center_x,center_y), r, (0, 255, 0), 2)    # draw found circle
                cv2.circle(cvOutImage, (center_x,center_y), 1, (0, 0, 255), 3)    # little circle at the found circle center
        
        return
    
    @staticmethod
    def EyesOnLine(eyes: list, line_start: Point, line_end: Point):
        """
        Check if a eye in eyes list is on a detection row of a domino stones.

        :param eyes: [description]
        :type eyes: list
        :param line_start: [description]
        :type line_start: Point
        :param line_end: [description]
        :type line_end: Point
        :return: [description]
        :rtype: [type]
        """

        eyes_on_line = []
        b = Point(x=line_end.X - line_start.X, y=line_end.Y - line_start.Y)
        a = Point(line_start.X, line_start.Y)
        b_val = np.sqrt(b.X * b.X + b.Y * b.Y)
               

        # d = |(p-a) x b| / |b|
        # crossproduct = pX * aY - pY * aX
        for eye in eyes:
            # 1
            if (eye['X'] <= line_start.X and eye['X'] >= line_end.X and eye['Y'] >= line_end.Y and eye['Y'] <= line_start.Y):
                pass
            # 2
            elif (eye['X'] >= line_start.X and eye['X'] <= line_end.X and eye['Y'] >= line_end.Y and eye['Y'] <= line_start.Y):
                pass
            # 3
            elif(eye['X'] <= line_start.X and eye['X'] >= line_end.X and eye['Y'] >= line_start.Y and eye['Y'] <= line_end.Y):
                pass
            # 4
            elif (eye['X'] >= line_start.X and eye['X'] <= line_end.X and eye['Y'] >= line_start.Y and eye['Y'] <= line_end.Y):
                pass
            else:
                continue
            
            
            d = np.abs(((a.X - eye['X']) * b.Y) - ((a.Y - eye['Y']) * b.X)) / b_val
            if d < eye['Radius']:
                eyes_on_line.append(eye)        
        
        return eyes_on_line
    
    @staticmethod
    def EyeDef(line1: list, line2: list, line3: list):
        """
        Define value of domino stone side by checking number of eyes
        on each detection line.

        :param line1: Detection line 1
        :type line1: list
        :param line2: Detection line 2 (center)
        :type line2: list
        :param line3: Detection line 3
        :type line3: list
        :return: Numerical eye value. Return None if no valid value found.
        :rtype: int | None
        """

        n_line1 = len(line1)
        n_line2 = len(line2)
        n_line3 = len(line3)

        if n_line1 == 0 and n_line2 == 1 and n_line3 == 0:
            return 1
        elif n_line1 == 1 and n_line2 == 0 and n_line3 == 1:
            return 2
        elif n_line1 == 1 and n_line2 == 1 and n_line3 == 1:
            return 3
        elif n_line1 == 2 and n_line2 == 0 and n_line3 == 2:
            return 4
        elif n_line1 == 2 and n_line2 == 1 and n_line3 == 2:
            return 5
        elif n_line1 == 3 and n_line2 == 0 and n_line3 == 3:
            return 6
        else:
            return None

    @staticmethod
    def EyeCounting(stones: list, eyes: list):
        """
        Get Value of right and left side of all domino-stones.

        :param stones: List of all DominoStone objects.
        :type stones: list
        :param eyes: lList of all detected circles.
        :type eyes: list
        """
        
        for stone in stones:
            stone.Eyes_Left.clear()
            stones_left_line1   = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Left.Line1[0], stone.ROI_Left.Line1[1])
            stones_left_line2   = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Left.Line2[0], stone.ROI_Left.Line2[1])
            stones_left_line3   = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Left.Line3[0], stone.ROI_Left.Line3[1])
            stone.Eyes_Left += stones_left_line1.copy()
            stone.Eyes_Left += stones_left_line2.copy()
            stone.Eyes_Left += stones_left_line3.copy()
            
            stone.Eyes_Right.clear()
            stones_right_line1  = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Right.Line1[0], stone.ROI_Right.Line1[1])
            stones_right_line2  = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Right.Line2[0], stone.ROI_Right.Line2[1])
            stones_right_line3  = DominoEyeDetection.EyesOnLine(eyes, stone.ROI_Right.Line3[0], stone.ROI_Right.Line3[1])
            stone.Eyes_Right += stones_right_line1.copy()
            stone.Eyes_Right += stones_right_line2.copy()
            stone.Eyes_Right += stones_right_line3.copy()

            stone.EyeVal_Left   = DominoEyeDetection.EyeDef(stones_left_line1, stones_left_line2, stones_left_line3)
            stone.EyeVal_Right  = DominoEyeDetection.EyeDef(stones_right_line1, stones_right_line2, stones_right_line3)

        return