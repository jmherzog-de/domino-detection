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

class GaussianBlurFilter(FilterBaseClass):
    """
    Filter Window to apply a gaussian blur filter.
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
        self.__kSize_cols, self.__kSize_rows = 0, 0
        self.__kSize_cols_max, self.__kSize_rows_max = 10, 10
        cv2.createTrackbar("kSize Cols", self._windowName, self.__kSize_cols, self.__kSize_cols_max, self.__onChange_kSizeCols)
        cv2.createTrackbar("kSize Rows", self._windowName, self.__kSize_rows, self.__kSize_rows_max, self.__onChange_kSizeRows)
        self.__action()
    
    def __onChange_kSizeCols(self, value):
        """
        Value changed event for parameter kSize_cols.
        The variable kSize_cols contains the value for the gaussian blur matrix cols size.

        :param value: Value of parameter kSizeCols
        :type value: [type]
        """
        self.__kSize_cols = value
        self.__action()

    def __onChange_kSizeRows(self, value):
        """
        Value changed event for parameter kSize_rows.
        THe variable kSizeRows contains the value for the gaussian blur matrix rows size.

        :param value: Value of parameter kSizeRows
        :type value: [type]
        """
        self.__kSize_rows = value
        self.__action()
    
    def Update(self, cvInputImage: np.ndarray):
        """
        Generate a filtered image with the new input image.

        :param cvInputImage: New OpenCV mat image.
        :type cvInputImage: np.ndarray
        """
        super().Update(cvInputImage)
        self.__action()
    
    def __action(self):
        """
        Generate new image.
        """
        if self.__kSize_rows == 0 or self.__kSize_cols == 0:
            self._cvProcImage = self._cvImage.copy()
            cv2.imshow(self._windowName, self._cvImage)
        else:
            self._cvProcImage   = cv2.GaussianBlur(self._cvImage, (self.__kSize_cols, self.__kSize_rows), 0)
            self._cvHist        = cv2.calcHist(self._cvProcImage, [0], None, [256], [0, 256])
            cv2.imshow(self._windowName, self._cvProcImage)
            self._callbackFct(self._cvProcImage)
        return
