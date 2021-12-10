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
import os

class AdaptiveThresholdWidget(BaseWidget):
    """
    Adaptive Threshold. This widget implement a adaptive threshold filter with OpenCV functions.
    The user has the ability to change the threshold.
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
        self.__blockSize    = int(os.environ.get('ADAPT_THRESH_BLOCK_SIZE'))
        self.__blockSizeMax = int(os.environ.get('ADAPT_THRESH_BLOCK_SIZE_MAX'))
        self.__C            = int(os.environ.get('ADAPT_THRESH_C'))
        self.__CMax         = int(os.environ.get('ADAPT_THRESH_CMAX'))
        self.AddSliderToGUI(name="Block Size", minVal=1, maxVal=self.__blockSizeMax, defaultVal=self.__blockSize, valueChangedCallback=self.blockSizeValueChanged)
        self.AddSliderToGUI(name="C", minVal=1, maxVal=self.__CMax, defaultVal=self.__C, valueChangedCallback=self.cValueChanged)

    def blockSizeValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: Current slider value.
        :type value: int
        """

        self.__blockSize = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def cValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider has changed.

        :param value: [description]
        :type value: int
        """
        
        self.__C = value
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
        self.OutputImage = cv2.adaptiveThreshold(cvInputImage, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY_INV, blockSize=self.__blockSize, C=self.__C)
        super().Action()
        return