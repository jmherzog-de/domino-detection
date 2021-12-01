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

from cv2 import NORMCONV_FILTER, clipLine
from .basewidget import BaseWidget, cv2, np
from domino_algorithms.eye_detection    import DominoEyeDetection


class AutoscaleWidget(BaseWidget):
    """
    Autoscaling brightness and contrast Widget. This widget implement a the hough circle detection method from the OpenCV library.
    The user has the ability to change the radius.
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
        self.OutputImage, alpha, beta = self.automatic_brightness_and_contrast(cvImage=cvInputImage, clip_hist_percent=25.0)
        super().Action()
        return
    

    def automatic_brightness_and_contrast(self, cvImage: np.ndarray, clip_hist_percent: float = 25.0):

        # Calculate grayscale histogram
        hist = cv2.calcHist(images=[cvImage], channels=[0], mask=None, histSize=[256], ranges=[0, 256])
        hist_size = len(hist)

        # Calculate cummulative distribution from histogram
        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index - 1] + float(hist[index]))
        
        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= maximum / 100.0
        clip_hist_percent /= 2.0

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1
                
        # Locate right cut
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
        
        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        auto_result = cv2.convertScaleAbs(cvImage, alpha=alpha, beta=beta)
        return (auto_result, alpha, beta)