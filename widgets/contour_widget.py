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

class ContourWidget(BaseWidget):
    """
    Contour findind widget. This widget implement a contour finding algorithm with OpenCV functions.
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

        self.__areaSizeMin = 10
        self.AddSliderToGUI(name="Area size minimum", minVal=self.__areaSizeMin, maxVal=2000, valueChangedCallback=self.onAreaSizeMinValueChanged)
    
    def onAreaSizeMinValueChanged(self, value: int) -> None:
        """
        Value changed event, triggered when the value of the slider 'Area size minimum' changed

        :param value: Current slider value.
        :type value: int
        """
        self.__areaSizeMin = value
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
        
        contours, _ = cv2.findContours(cvInputImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        self.OutputImage = self.OriginalImage.copy()
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area >= self.__areaSizeMin:

                eps = 0.05 * cv2.arcLength(cnt, True)
                approx  = cv2.approxPolyDP(curve=cnt, epsilon=eps, closed=True)
                
                cv2.drawContours(self.OutputImage, cnt, -1, (255, 0, 255), 3)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(self.OutputImage, [box], 0, (0,0,255), thickness=2)
                

        
        super().Action()

        return
    