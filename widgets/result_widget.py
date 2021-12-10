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

from .basewidget import BaseWidget, cv2, np
from domino_algorithms.divider_extraction import DividerExtraction
from domino_algorithms.eye_detection    import DominoEyeDetection
from domino_algorithms.roi_approx import RoiApprox
import os

class ResultWidget(BaseWidget):
    """
    The processing result widget. This widget sum up all processing steps and results the final image.
    """

    def __init__(self, availableFilterWidgets: list, widgetName: str, cvOriginalImage: np.ndarray, videoMode: bool = False, defaultFilterWidget: str = "Original Image", parameterChangedCallback=None) -> None:
        """
        Constructor method.

        :param availableFilterWidgets: List with all available widgets.
        :type availableFilterWidgets: list
        :param widgetName: The name of this widget. This is also the window name.
        :type widgetName: str
        :param cvOriginalImage: Original image read from OpenCV method.
        :type cvOriginalImage: np.ndarray
        :param videoMode: [description], defaults to False
        :type videoMode: bool, optional
        :param defaultFilterWidget: Default input image to apply filter, defaults to "Original Image"
        :type defaultFilterWidget: str, optional
        :param parameterChangedCallback: Callback function for widget slider value changed, defaults to None
        :type parameterChangedCallback: [type], optional
        """
        super().__init__(availableFilterWidgets, widgetName, cvOriginalImage, videoMode=videoMode, defaultFilterWidget=defaultFilterWidget, parameterChangedCallback=parameterChangedCallback)

        self.__minRadius    = int(os.environ.get('CIRCLE_DETECT_MIN_RADIUS'))
        self.__maxRadius    = int(os.environ.get('CIRCLE_DETECT_MAX_RADIUS'))
        self.__param1       = int(os.environ.get('CIRCLE_DETECT_PARAM_1'))
        self.__param2       = int(os.environ.get('CIRCLE_DETECT_PARAM_2'))
        self.__minDist      = int(os.environ.get('CIRCLE_DETECT_MIN_DIST'))
        self.__param1Max    = int(os.environ.get('CIRCLE_DETECT_PARAM_1_MAX'))
        self.__param2Max    = int(os.environ.get('CIRCLE_DETECT_PARAM_2_MAX'))
        self.__minRadiusMax = int(os.environ.get('CIRCLE_DETECT_MIN_RADIUS_MAX'))
        self.__maxRadiusMax = int(os.environ.get('CIRCLE_DETECT_MAX_RADIUS_MAX'))
        self.__minDistMax   = int(os.environ.get('CIRCLE_DETECT_MIN_DIST_MAX'))
        self.__minArea      = int(os.environ.get('FIND_DIV_AREA_MIN'))
        self.AddSliderToGUI(name="Min Radius", minVal=1, maxVal=self.__minRadiusMax, defaultVal=self.__minRadius, valueChangedCallback=self.minRadiusValueChanged)
        self.AddSliderToGUI(name="Max Radius", minVal=1, maxVal=self.__maxRadiusMax, defaultVal=self.__maxRadius, valueChangedCallback=self.maxRadiusValueChanged)
        self.AddSliderToGUI(name="Param 1", minVal=1, maxVal=self.__param1Max, defaultVal=self.__param1, valueChangedCallback=self.param1ValueChanged)
        self.AddSliderToGUI(name="Param 2", minVal=1, maxVal=self.__param2Max, defaultVal=self.__param2, valueChangedCallback=self.param2ValueChanged)
        self.AddSliderToGUI(name="Min Distance", minVal=1, maxVal=self.__minDistMax, defaultVal=self.__minDist, valueChangedCallback=self.minDistValueChanged)
    
    def minDistValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: [description]
        :type value: int
        """

        self.__minDist = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)

    def minRadiusValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: Current slider value.
        :type value: int
        """

        self.__minRadius = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def maxRadiusValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: [description]
        :type value: int
        """
        
        self.__maxRadius = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def param1ValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: [description]
        :type value: int
        """

        self.__param1 = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def param2ValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: [description]
        :type value: int
        """

        self.__param2 = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def ComboBoxInputImageChanged(self, index: int) -> None:
        """
        Triggered when the selected index changed of the input combobox.

        :param index: selected item index
        :type index: int
        """
        super().ComboBoxInputImageChanged(index)
        self.Action()
        return
    
    def Action(self):
        """
        Apply filter on input image.
        """
        
        cvInputImage:np.ndarray = self.SelectInputImage()
        self.OutputImage = self.OriginalImage.copy()
        stones = DividerExtraction.ExtractDividers(cvImage=cvInputImage.copy(), minArea=self.__minArea, cvOutImage=self.OutputImage)
        RoiApprox.FindROI(stones, cvOutImage=self.OutputImage)
        domino_eyes = DominoEyeDetection.ExtractEyes(cvImage=cvInputImage, cvOutImage=self.OutputImage, min_dist=self.__minDist, param_1=self.__param1, param_2=self.__param2, min_radius=self.__minRadius, max_radius=self.__maxRadius)
        DominoEyeDetection.EyeCounting(stones, domino_eyes)

        super().Action()
        return