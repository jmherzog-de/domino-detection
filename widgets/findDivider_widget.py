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

from domino_algorithms.roi_approx import RoiApprox
from .basewidget import BaseWidget, cv2, np
from domino_algorithms.divider_extraction import DividerExtraction


class FindDividerWidget(BaseWidget):
    """
    Widget to extract the divider rectangle from the domino stones.
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

        self.__areaSizeMin = 700
    
    def onAreaSizeMinValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider 'Area size minimum' changed

        :param value: Current slider value.
        :type value: int
        """
        self.__areaSizeMin = 700
        self.Action()
        self.ValueChangedCallbackWrapper(value)
    
    def ComboBoxInputImageChanged(self, index: int) -> None:
        """
        Triggered when the selected index changed of the input combobox.

        :param index: [description]
        :type index: [type]
        """
        super().ComboBoxInputImageChanged(index)
        self.Action()
        return
    
    def Action(self) -> None:
        """
        Apply contour finding algorithm on input image.
        """

        cvInputImage:np.ndarray = self.SelectInputImage()
        #self.OutputImage = np.zeros(self.OriginalImage.shape, dtype='uint8')
        self.OutputImage = self.OriginalImage.copy()
        divs = DividerExtraction.ExtractDividers(cvImage=cvInputImage.copy(), cvOutImage=self.OutputImage)
        #RoiApprox.FindROI(divs, cvOutImage=self.OutputImage)
            
                
        super().Action()

        return
    