"""
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
 """

import cv2
import numpy as np
from filter_base_class import FilterBaseClass


class CannyFilter(FilterBaseClass):
    """
    Filter Window to apply a canny edge detection.
    """

    def __init__(self, cvWindowName: str, cvWindowTitle: str, cvInputImage: np.ndarray, imageUpdateEventCallbackFct) -> None:
        """
        Class Constructor generate OpenCV image  overloading the FilterBaseClass.

        :param cvWindowName: Unique name of the UI window.
        :type cvWindowName: str
        :param cvWindowTitle: Window title displayed on the top of the window.
        :type cvWindowTitle: str
        :param cvInputImage: OpenCV mat image input
        :type cvInputImage: np.ndarray
        :param imageUpdateEcentCallback: Callback function get called when some parameter of the filter has changed.
        :type imageUpdateEcentCallback: [type]
        """
        super().__init__(cvWindowName, cvWindowTitle, cvInputImage, imageUpdateEventCallbackFct)
        self.__threshMin        = 100
        self.__threshMax        = 200
        self.__thresMaxValue    = 255
        cv2.createTrackbar("Threshold Min.", self._windowName, self.__threshMin, self.__thresMaxValue, self.__thresholdMinChanged)
        cv2.createTrackbar("Threshold Max.", self._windowName, self.__threshMax, self.__thresMaxValue, self.__thresholdMaxChanged)
        self.__action()
    
    def __thresholdMinChanged(self, value):
        """
        Value for minimum threshold value changed.

        :param value: Slider value for minimum threshold.
        :type value: [type]
        """
        self.__threshMin = value
        self.__action()
    
    def __thresholdMaxChanged(self, value):
        """
        Value for maximum threshold value changed.

        :param value: Slider value for maximum threshold.
        :type value: [type]
        """
        self.__threshMax = value
        self.__action()
    
    def Update(self, cvInputImage: np.ndarray):
        """
        Generate filtered image with new input OpenCV mat image.

        :param cvInputImage: New OpenCV mat image.
        :type cvInputImage: np.ndarray
        """
        super().Update(cvInputImage)
        self.__action()
    
    def __action(self):
        """
        Generate image.
        """
        self._cvProcImage = cv2.Canny(self._cvImage, self.__threshMin, self.__threshMax)
        self._cvHist = cv2.calcHist(self._cvProcImage, [0], None, [256], [0, 256])
        cv2.imshow(self._windowName, self._cvProcImage)
        self._callbackFct(self._cvProcImage)