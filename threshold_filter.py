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

class ThresholdFilter(FilterBaseClass):
    """
    Filter Window to apply an binary threshold filter.
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
        self.__thresh       = 50
        self.__thresh_max   = 255
        cv2.createTrackbar("Threshold", self._windowName, self.__thresh, self.__thresh_max, self.__onChange_Threshold)
        self.__action()
    
    def __onChange_Threshold(self, value):
        """
        Threshold value changed.

        :param value: New threshold value from slider.
        :type value: [type]
        """
        self.__thresh = value
        self.__action()
    
    def Update(self, cvInputImage: np.ndarray):
        """
        Generate a filtered image from new input OpenCV mat image.

        :param cvInputImage: New OpenCV mat image.
        :type cvInputImage: np.ndarray
        """
        super().Update(cvInputImage)
        self.__action()
    
    def __action(self):
        """
        Generate new image.
        """
        self.__thresh, self._cvProcImage   = cv2.threshold(self._cvImage, self.__thresh, 255, cv2.THRESH_BINARY)
        self._cvHist        = cv2.calcHist(self._cvProcImage, [0], None, [256], [0, 256])
        cv2.imshow(self._windowName, self._cvProcImage)
        self._callbackFct(self._cvProcImage)