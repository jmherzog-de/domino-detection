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

from .basewidget        import BaseWidget, cv2, np
from domino_algorithms import DominoEyeDetection


class ResultWidget(BaseWidget):
    """
    Final processing widget. This widget combine the detected circles with the detected domino stones.
    """

    def __init__(self, availableFilterWidgets: list, widgetName: str, cvOriginalImage: np.ndarray, videoMode: bool = False, defaultFilterWidget: str = "Original Image", stones: list = [], eyes: list = [], parameterChangedCallback=None) -> None:
        """
        Constructor method.

        :param availableFilterWidgets: List with all available widgets.
        :type availableFilterWidgets: list
        :param widgetName: The name of this widget. This is also the window name.
        :type widgetName: str
        :param cvOriginalImage: Original image read from OpenCV method.
        :type cvOriginalImage: np.ndarray
        :param videoMode: Enabled video mode True := active False := disabled, defaults to False
        :type videoMode: bool, optional
        :param defaultFilterWidget: Default input image to apply filter, defaults to "Original Image"
        :type defaultFilterWidget: str, optional
        :param stones: List with all detected stones as DominoStone objects, defaults to []
        :type stones: list, optional
        :param eyes: List of dicts with all detected eyes, defaults to []
        :type eyes: list, optional
        :param parameterChangedCallback: Callback function for widget slider value changed, defaults to None
        :type parameterChangedCallback: [type], optional
        """
        super().__init__(availableFilterWidgets, widgetName, cvOriginalImage, videoMode=videoMode, defaultFilterWidget=defaultFilterWidget, parameterChangedCallback=parameterChangedCallback)
        self.__stones       = stones
        self.__eyes         = eyes
    
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
        Count eyes on domino stone detection line.
        Draw the circles on screen and value for each side.
        """
        
        self.OutputImage = self.OriginalImage.copy()
        DominoEyeDetection.EyeCounting(self.__stones, self.__eyes)

        for stone in self.__stones:
            cv2.putText(self.OutputImage, str(stone.EyeVal_Left), org=(stone.ROI_Left.Line1[1].X+20, stone.ROI_Left.Line1[1].Y+20), fontScale=1, color=(255, 0, 0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=3)
            for eye in stone.Eyes_Left:
                cv2.circle(self.OutputImage, center=(eye['X'], eye['Y']), radius=eye['Radius'], color=(0,255,0), thickness=3)
            
            cv2.putText(self.OutputImage, str(stone.EyeVal_Right), org=(stone.ROI_Right.Line1[1].X+20, stone.ROI_Right.Line1[1].Y+20), fontScale=1, color=(255, 0, 0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=3)

        super().Action()
        return