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

from PySide6.QtCore     import QSize, Qt
from PySide6.QtWidgets  import QComboBox, QGridLayout, QGroupBox, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui      import QImage, QPixmap

from .sliderwidget      import SliderWidget

import numpy as np
import cv2

class BaseWidget(QWidget):
    """
    Base Class implement the Qt Filter Widget User Interface.

    :param QWidget: Class Object of QWidget
    :type QWidget: object
    """

    def __init__(self, availableFilterWidgets: list, widgetName: str, cvOriginalImage: np.ndarray, videoMode: bool = False, defaultFilterWidget: str = "Original Image", parameterChangedCallback = None) -> None:
        """
        Class Constructor. This Constructor implements the whole Qt GUI for the filter widgets.

        :param availableFilterWidgets: List with all available widgets.
        :type availableFilterWidgets: list
        :param widgetName: The name of this widget. This is also the window name.
        :type widgetName: str
        :param cvOriginalImage: Original image read from OpenCV mehtod.
        :type cvOriginalImage: np.ndarray
        :param videoMode: Set the widget into video mode or picture mode, defaults to False (disabled video mode)
        :type videoMode: bool, optional
        :param defaultFilterWidget: Default input image to apply filter defaults to "Original Image"
        :type defaultFilterWidget: str, optional
        :param parameterChangedCallback: Callback function for widget slider value changed, defaults to None
        :type parameterChangedCallback: function reference, optional
        """

        super().__init__()
        
        self.__defaultFilterWidget      = defaultFilterWidget
        self.__parameterChangedCallback = parameterChangedCallback
        self.__activeFilterWidget       = defaultFilterWidget
        self.__widgetName               = widgetName
        self.__availableFilterWidgets   = availableFilterWidgets
        self.__cvOriginalImage          = cvOriginalImage
        self.__cvOutputImage            = cvOriginalImage
        self.__videoMode                = videoMode
        self.resizeEvent                = self.onResize

        self.setupUi()
        
        return

    
    def setupUi(self) -> None:
        """
        Setup Qt GUI
        """

        self.centralWidget  = QWidget(self)
        self.centralWidget.setObjectName(u"centralWidget")
        self.setWindowTitle(self.WidgetName)

        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.inputImageGroupBox = QGroupBox(self.centralWidget)
        self.inputImageGroupBox.setObjectName(u"inputImageGroupBox")
        self.inputImageGroupBox.setTitle(u"Input Image")
        self.inputImageGroupBox.setMaximumHeight(100)

        self.gridLayout = QGridLayout(self.inputImageGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")

        self.comboBoxInputImage = QComboBox(self.inputImageGroupBox)
        self.comboBoxInputImage.setObjectName(u"comboBoxInputImage")
        self.comboBoxInputImage.currentIndexChanged.connect(self.ComboBoxInputImageChanged)
        
        self.gridLayout.addWidget(self.comboBoxInputImage, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.inputImageGroupBox)

        self.parametersGroupBox = QGroupBox(self.centralWidget)
        self.parametersGroupBox.setObjectName(u"parametersGroupBox")
        self.parametersGroupBox.setTitle(u"Parameter")

        self.gridLayout_2 = QGridLayout(self.parametersGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.parametersLayout = QVBoxLayout()
        self.parametersLayout.setObjectName(u"parametersLayout")
        self.gridLayout_2.addLayout(self.parametersLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.parametersGroupBox)

        self.imageGroupBox = QGroupBox(self.centralWidget)
        self.imageGroupBox.setObjectName(u"imageGroupBox")
        self.imageGroupBox.setTitle(u"Output Image")

        self.gridLayout_3 = QGridLayout(self.imageGroupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.image = QLabel(self.imageGroupBox)
        self.image.setObjectName(u"image")
        self.image.setMinimumSize(QSize(500, 500))
        self.image.setStyleSheet(u"background-color: rgb(0,0,0);")
        self.image.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.image, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.imageGroupBox)
        self.setLayout(self.verticalLayout)

        return
    

    @property
    def VideoMode(self) -> bool:
        return bool(self.__videoMode)
    
    @VideoMode.setter
    def VideoMode(self, videoEnabled: bool) -> None:
        if not isinstance(videoEnabled, bool):
            raise Exception("Invalid input type for 'VideoMode'.")
        self.__videoMode = True
    
    @property
    def DefaultWidgetName(self) -> str:
        return self.__defaultFilterWidget
    
    @DefaultWidgetName.setter
    def DefaultWidgetName(self, name: str) -> None:
        if not isinstance(name, str):
            raise Exception("Invalid input type for 'DefaultWidgetName'.")
        self.__defaultFilterWidget = name
    
    @property
    def WidgetName(self) -> str:
        return self.__widgetName
    
    @WidgetName.setter
    def WidgetName(self, name: str) -> None:
        if not isinstance(name, str):
            raise Exception("Invalid input type for 'WidgetName'.")
        self.__widgetName = name

    @property
    def ParamChangedCallback(self):
        return self.__parameterChangedCallback
    
    @property
    def ActiveFilterWidget(self) -> str:
        return self.__activeFilterWidget
    
    @ActiveFilterWidget.setter
    def ActiveFilterWidget(self, name: str) -> None:
        if not isinstance(name, str):
            raise Exception("Invalid input type for 'ActiveFilterWidget'.")
        self.__activeFilterWidget = name
    
    @property
    def AvailableFilterWidgets(self) -> list:
        return self.__availableFilterWidgets
    
    @property
    def OriginalImage(self) -> np.ndarray:
        return self.__cvOriginalImage
    
    @OriginalImage.setter
    def OriginalImage(self, cvImage: np.ndarray) -> None:
        if not isinstance(cvImage, np.ndarray):
            raise Exception("Invalid input type for 'OriginalImage'.")
        self.__cvOriginalImage = cvImage
    
    @property
    def OutputImage(self) -> np.ndarray:
        return self.__cvOutputImage
    
    @OutputImage.setter
    def OutputImage(self, cvImage: np.ndarray) -> None:
        if not isinstance(cvImage, np.ndarray):
            raise Exception("Invalid input type for 'OutputImage'.")
        self.__cvOutputImage = cvImage


    def show(self) -> None:
        """
        Display widget window.
        This method override the default Qt show function
        and fill the combobox with all available filter names.
        """

        self.comboBoxInputImage.clear()
        self.comboBoxInputImage.addItem("Original Image")
        for filter in self.AvailableFilterWidgets:
            if filter.WidgetName == self.WidgetName:
                continue
            self.comboBoxInputImage.addItem(filter.WidgetName)
            self.comboBoxInputImage.setCurrentText(self.ActiveFilterWidget)

        return super().show()


    def onResize(self, event) -> None:
        """
        Qt resize event method.
        """
        if not self.VideoMode: self.Action()


    def ConvertCvToQt(self, cvImage: np.ndarray) -> QImage:
        """
        Convert a image from OpenCV numpy array into Qt QImage.

        :param cvImage: Input image
        :type cvImage: np.ndarray
        :return: Converted and scaled output image
        :rtype: QImage
        """
        
        if len(cvImage.shape) == 2:
            h,w = cvImage.shape
            bytes_per_line  = w
            qImage = QImage(cvImage.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        else:
            h,w,c = cvImage.shape
            bytes_per_line = c * w
            qImage = QImage(cvImage.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        return qImage.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio)


    def ComboBoxInputImageChanged(self, index: int):
        """
        Event method get called, when the selected filter changed.

        :param index: active combobox index
        :type index: int
        """
        if not self.isActiveWindow():
            return
        
        if self.ActiveFilterWidget == None:
            self.ActiveFilterWidget = self.DefaultWidgetName
        
        text = self.comboBoxInputImage.itemText(index)
        if text == "Original Image":
            self.ActiveFilterWidget = "Original Image"
        else:
            self.ActiveFilterWidget = self.comboBoxInputImage.itemText(index)
        
        return


    def ValueChangedCallbackWrapper(self, value: int) -> None:
        """
        Wrapper callback function to update output image, when other
        widget parameter changed.
        This is only executed in photo mode.

        :param value: New parameter value
        :type value: int
        """
        if not self.VideoMode:
            self.Action()
            self.__parameterChangedCallback()


    def AddSliderToGUI(self, name: str, minVal: int = 0, maxVal: int = 255, defaultVal: int = 0, valueChangedCallback = None) -> None:
        """
        Create a new Slider Widget into the Parameters GroupBox.

        :param name: Parameter name
        :type name: str
        :param minVal: slider min value, defaults to 0
        :type minVal: int, optional
        :param maxVal: slider max value, defaults to 255
        :type maxVal: int, optional
        :param defaultVal: slider default value, defaults to 0
        :type defaultVal: int, optional
        :param valueChangedCallback: Callback event that gets called when the slider value has changed, defaults to None
        :type valueChangedCallback: function reference, optional
        """
        slider = SliderWidget(name=name, min=minVal, max=maxVal, defaultValue=defaultVal, onChangeCallback=valueChangedCallback)
        self.parametersLayout.addWidget(slider)
        return


    def SelectInputImage(self) -> np.ndarray:
        """
        Select the currently active input image for the filter widget.

        :raises Exception: Image is not a valid numpy array.
        :return: Active input image reference from widget
        :rtype: np.ndarray
        """
        
        cvInputImage: np.ndarray    = None

        if self.ActiveFilterWidget  == "Original Image":
            cvInputImage    = self.OriginalImage
        else:
            for widget in self.AvailableFilterWidgets:
                if widget.WidgetName    == self.ActiveFilterWidget:
                    cvInputImage = widget.OutputImage
                    break
        
        if not isinstance(cvInputImage, np.ndarray):
            raise Exception("Image is not a numpy array.")
        
        return cvInputImage


    def Action(self):
        """
        Convert image and display it.
        """
        
        if isinstance(self.__cvOutputImage, np.ndarray):
            qImage = self.ConvertCvToQt(self.__cvOutputImage)
            self.image.setPixmap(QPixmap.fromImage(qImage))
        return