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

import sys
import cv2
import numpy as np

from blur_filter            import BlurFilter
from gaussian_blur_filter   import GaussianBlurFilter
from threshold_filter       import ThresholdFilter
from canny_filter           import CannyFilter


class ImageMode(object):
    """
    Application image mode class.
    All filter will be applied onto a single image from filepath.
    """

    def __init__(self, file_path:str) -> None:
        """
        Class constructor open image from filepath and convert into grayscale image.

        :param file_path: path to image
        :type file_path: str
        """
        self.__cvOriginalImage  = cv2.imread(file_path)
        self.__cvGrayscaleImage = cv2.cvtColor(self.__cvOriginalImage, cv2.COLOR_BGR2GRAY)
        self.__cvGrayscaleHist  = cv2.calcHist(self.__cvGrayscaleImage, [0], None, [256], [0, 256])

        self.__blurFilter           = None
        self.__gaussianBlurFilter   = None
        self.__threshFilter         = None
        self.__cannyFilter          = None
    
    def __onChange_BlurFilter(self, cvImage:np.ndarray):
        """
        Callback Event when filter parameter of the blur filter has changed.

        :param cvImage: New filtered image.
        :type cvImage: np.ndarray
        """
        if self.__gaussianBlurFilter != None: self.__gaussianBlurFilter.Update(cvImage)

    def __onChange_GaussianBlur(self, cvImage:np.ndarray):
        """
        Callback Event when filter parameter of the gaussian blur filter has chagned.

        :param cvImage: New filtered image.
        :type cvImage: np.ndarray
        """
        if self.__threshFilter != None: self.__threshFilter.Update(cvImage)

    def __onChange_Threshold(self, cvImage:np.ndarray):
        """
        Callback Event when filtered parameter for the threshold filter has changed.

        :param cvImage: New filtered image.
        :type cvImage: np.ndarray
        """
        if self.__cannyFilter != None: self.__cannyFilter.Update(cvImage)

    def __onChange_Canny(self, cvImage:np.ndarray):
        """
        Callback Event when filtered parameter for the canny edge detection has changed.

        :param cvImage: New filtered image.
        :type cvImage: np.ndarray
        """

    def Run(self):
        """
        Generate all windows and show the images.
        Application halt there until any key is pressed.
        """
        self.__blurFilter           = BlurFilter("blur_filter", "Blur Filter", self.__cvGrayscaleImage, self.__onChange_BlurFilter)
        self.__gaussianBlurFilter   = GaussianBlurFilter("gaus_blur", "Gaussian Blur Filter", self.__blurFilter.GetImage(), self.__onChange_GaussianBlur)
        self.__threshFilter         = ThresholdFilter("thresh_filter", "Threshold Filter", self.__blurFilter.GetImage(), self.__onChange_Threshold)
        self.__cannyFilter          = CannyFilter("canny", "Canny Filter", self.__threshFilter.GetImage(), self.__onChange_Canny)
        cv2.waitKey(0)


if __name__ == '__main__':

    #application_mode    = int(sys.argv[1])
    #image_path          = str(sys.argv[2])
    application_mode = 0
    
    if application_mode == 0:
        ImageMode(file_path="images/1.jpeg").Run()
    elif application_mode == 1:
        print("Video mode not implemented.")
    else:
        print("invalid operation mode selected.")
    
    exit(0)