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

from .basewidget    import BaseWidget, cv2, np


class CannyWidget(BaseWidget):
    """
    Canny Filter widget. This widget implement the canny edge detection algorithm with OpenCV functions.
    The user has the ability to change upper and lower thresholds.
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
        self.__threshold1   = 90
        self.__threshold2   = 120
        self.AddSliderToGUI(name="threshold 1", defaultVal=self.__threshold1, valueChangedCallback=self.threshold1ValueChanged)
        self.AddSliderToGUI(name="threshold 2", defaultVal=self.__threshold2, valueChangedCallback=self.threshold2ValueChanged)
    
    def threshold1ValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the lower threshold value has changed.

        :param value: Current slider value
        :type value: int
        """
        self.__threshold1 = value
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def threshold2ValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the upper threshold value has changed.

        :param value: Current slider value
        :type value: int
        """
        self.__threshold2 = value
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
    
    def Action(self) -> None:
        """
        Apply canny algorithm on input image.
        """

        cvInputImage:np.ndarray = self.SelectInputImage()
        self.OutputImage = cv2.Canny(cvInputImage, self.__threshold1, self.__threshold2)
        super().Action()
        return