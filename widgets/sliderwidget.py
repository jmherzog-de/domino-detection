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

from PySide6.QtCore     import Qt
from PySide6.QtWidgets  import QGridLayout, QLabel, QSlider, QVBoxLayout, QWidget

class SliderWidget(QWidget):
    """
    Qt Slider Widget for filter parameters.

    :param QWidget: Base Class
    :type QWidget: QWidget
    """

    def __init__(self, name: str, min: int = 0, max: int = 255, defaultValue: int = 0, onChangeCallback = None) -> None:
        """
        Class constructor.

        :param name: Parameter name
        :type name: str
        :param min: Parameter minimum value, defaults to 0
        :type min: int, optional
        :param max: Parameter maximum value, defaults to 255
        :type max: int, optional
        :param defaultValue: Parameter default value, defaults to 0
        :type defaultValue: int, optional
        :param onChangeCallback: Callback function get called on value chaned, defaults to None
        :type onChangeCallback: function, optional
        """
        super().__init__()

        self.__min     = min
        self.__max     = max
        self.__defaultValue = defaultValue
        self.__name         = name

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        self.parameterName = QLabel(self)
        self.parameterName.setObjectName(u"parameterName")
        self.parameterName.setText(self.__name)
        self.verticalLayout.addWidget(self.parameterName)

        self.parameterSlider = QSlider(self)
        self.parameterSlider.setObjectName(u"parameterSlider")
        self.parameterSlider.setMinimum(self.__min)
        self.parameterSlider.setMaximum(self.__max)
        self.parameterSlider.setValue(self.__defaultValue)
        self.parameterSlider.setOrientation(Qt.Horizontal)
        if onChangeCallback != None:
            self.parameterSlider.valueChanged.connect(onChangeCallback)
            self.parameterSlider.valueChanged.connect(self.__onChangedInternalCallback)

        self.verticalLayout.addWidget(self.parameterSlider)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        
        self.minValue = QLabel(self)
        self.minValue.setObjectName(u"minValue")
        self.minValue.setText(str(self.__min))
        self.gridLayout.addWidget(self.minValue, 0, 1, 1, 1, Qt.AlignLeft)

        self.maxValue = QLabel(self)
        self.maxValue.setObjectName(u"maxValue")
        self.maxValue.setText(str(self.__max))
        self.gridLayout.addWidget(self.maxValue, 0, 1, 1, 1, Qt.AlignRight)

        self.value = QLabel(self)
        self.value.setObjectName(u"value")
        self.value.setText(str(self.__defaultValue))

        self.gridLayout.addWidget(self.value, 0, 1, 1, 1, Qt.AlignHCenter)

        self.verticalLayout.addLayout(self.gridLayout)
    
    def __onChangedInternalCallback(self, value: int) -> None:
        """
        Update value on screen when the slider value changed.

        :param value: New slider value.
        :type value: int
        """
        self.value.setText(str(value))
