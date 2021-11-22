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

from PySide6.QtCore         import QRect, QSize, QThread, Qt, Signal, Slot
from PySide6.QtGui          import QAction, QImage, QPixmap
from PySide6.QtWidgets      import QFileDialog, QGridLayout, QGroupBox, QLabel, QListWidget, QListWidgetItem, QMainWindow, QMenu, QMenuBar, QStatusBar, QVBoxLayout, QWidget
import numpy    as np
import widgets  as UIWidgets
import cv2

from widgets import contour_widget

class VideoThread(QThread):
    """
    OpenCV video capture thread.

    :param QThread: Base implementations for QThread.
    """
    updateFrame = Signal(np.ndarray)

    def __init__(self, parent=None) -> None:
        """
        Constructor function. Initialize status variable and
        capture variable.

        :param parent: No parent Widget, defaults to None
        """
        QThread.__init__(self, parent)
        self.status = True
        self.cap    = True
    
    def run(self):
        """
        Run capturing process. This method capture a frame
        from the camera and convert it from BGR to RGB.
        This method emit a signal on every successfull frame capture.
        """

        self.cap = cv2.VideoCapture(0)
        while self.status:
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.updateFrame.emit(frame)


class MainWindow(QMainWindow):
    """
    Main window implementation.

    :param QMainWindow: Qt MainWindow Base class.
    :type QMainWindow: QMainWindow
    """

    def __init__(self) -> None:
        """
        UI implementation of the main window.
        """

        super().__init__()
        self.__cvOriginalImage  = None
        self.__qtOriginalImage  = None
        self.__videoMode        = False
        self.__availableFilters = list()

        self.setupUi()
    

    def setupUi(self):
        """
        Implement Qt GUI.
        """

        self.setWindowTitle("Domino Detection - Calibration Software")
        self.setGeometry(0, 0, 800 ,600)

        #
        # Qt Actions
        #
        self.action_WebcamStream = QAction(self)
        self.action_WebcamStream.setText(u"Webcam Stream")
        self.action_WebcamStream.setObjectName(u"action_WebcamStream")
        self.action_WebcamStream.triggered.connect(self.onWebcamModeClicked)

        self.action_PhotoMode = QAction(self)
        self.action_PhotoMode.setText(u"Photo Mode")
        self.action_PhotoMode.setObjectName(u"action_PhotoMode")
        self.action_PhotoMode.triggered.connect(self.onPhotoModeClicked)

        self.action_Close = QAction(self)
        self.action_Close.setText(u"Close Application")
        self.action_Close.setObjectName(u"action_Close")
        self.action_Close.triggered.connect(self.onCloseClicked)

        #
        # Layouts
        #
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralWidget")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.centralwidget.setObjectName(u"verticalLayout")

        #
        # Filters Group Box
        #
        self.filterGroupbox = QGroupBox(self.centralwidget)
        self.filterGroupbox.setTitle(u"Available Filters")
        self.filterGroupbox.setMaximumHeight(250)
        self.filterGroupbox.setObjectName(u"filterGroupbox")
        self.gridLayout     = QGridLayout(self.filterGroupbox)
        self.filterListBox  = QListWidget(self.filterGroupbox)
        self.filterListBox.setEnabled(False)
        self.filterListBox.setObjectName(u"filterListBox")
        
        self.filterListBox.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.addWidget(self.filterListBox, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.filterGroupbox)

        #
        # Image Groupbox
        #
        self.imageGroupbox = QGroupBox(self.centralwidget)
        self.imageGroupbox.setTitle(u"Original Image")
        self.imageGroupbox.setObjectName(u"imageGroupbox")
        self.gridLayout_2 = QGridLayout(self.imageGroupbox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.image = QLabel(self.imageGroupbox)
        self.image.setText(u"IMAGE")
        self.image.setObjectName(u"image")
        self.image.setMinimumSize(QSize(350, 350))
        self.image.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.image.setAlignment(Qt.AlignCenter)    
        self.gridLayout_2.addWidget(self.image, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.imageGroupbox)  

        self.setCentralWidget(self.centralwidget)
        self.mainMenuBar = QMenuBar(self)
        self.mainMenuBar.setObjectName(u"mainMenuBar")
        self.mainMenuBar.setGeometry(QRect(0, 0, 800, 24))
        self.mainMenu = QMenu(self.mainMenuBar)
        self.mainMenu.setObjectName(u"mainMenu")
        self.mainMenu.setTitle(u"Source")
        self.setMenuBar(self.mainMenuBar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.mainMenuBar.addAction(self.mainMenu.menuAction())
        self.mainMenu.addAction(self.action_WebcamStream)
        self.mainMenu.addAction(self.action_PhotoMode)
        self.mainMenu.addAction(self.action_Close)
    
    def __convert_cv_qt(self, cvImage:np.ndarray):
        """
        Convert OpenCV image into QImage and scale it to the
        size of the image label.

        :param cvImage: OpenCV input image
        :type cvImage: np.ndarray
        :return: Converted and scaled image.
        :rtype: QImage
        """
        h, w, c = cvImage.shape
        bytes_per_line = c * w
        convert_to_Qt_format = QImage(cvImage.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio)
        return p
    
    @Slot()
    def onCloseClicked(self):
        """
        Qt Event on close application.
        """
        self.close()
    
    @Slot()
    def onPhotoModeClicked(self):
        """
        Open photo from filesystem.
        """

        self.__videoMode = False
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open image")
        if fileName:
            self.filterListBox.setEnabled(True)
            self.__cvOriginalImage = cv2.imread(fileName)
            self.__cvOriginalImage = cv2.cvtColor(self.__cvOriginalImage, cv2.COLOR_BGR2RGB)
            self.__qtOriginalImage = self.__convert_cv_qt(self.__cvOriginalImage)
            self.image.setPixmap(QPixmap.fromImage(self.__qtOriginalImage))
            self.InitFilter()

    @Slot()
    def onWebcamModeClicked(self):
        """
        Open Video Stream from Webcam.
        """

        self.__videoMode = True
        self.filterListBox.setEnabled(True)
        self.webcamThread   = VideoThread(self)
        self.webcamThread.finished.connect(self.close)
        self.webcamThread.updateFrame.connect(self.UpdateImage)
        self.webcamThread.start()
        self.InitFilter()
    
    @Slot()
    def itemDoubleClicked(self, item:QListWidgetItem):
        """
        Qt event triggered when the listbox item double clicked.

        :param item: double clicked listbox item.
        :type item: QListWidgetItem
        """
        for widget in self.__availableFilters:
            if widget.WidgetName == item.text():
                widget.show()
                widget.Action()
                return

    @Slot()
    def UpdateImage(self, cvFrame:np.ndarray):
        """
        Update image to display on screen.
        This method is used only in video mode.

        :param cvFrame: OpenCV input image.
        :type cvFrame: np.ndarray
        """

        qImage = self.__convert_cv_qt(cvFrame.copy())
        self.image.setPixmap(QPixmap.fromImage(qImage))
        for widget in self.__availableFilters:
            widget.OriginalImage = cvFrame.copy()
            widget.Action()
    
    def parameterChangedCallback(self):
        
        for widget in self.__availableFilters:
            widget.Action()

    def InitFilter(self):
        """
        Initialize filters.

        TODO: Implement all filters here.
        """

        grayscale_filter    = UIWidgets.GrayscaleWidget(videoMode=self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="GRAYSCALE FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="Original Image", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(grayscale_filter)

        blur_filter         = UIWidgets.BlurWidget(videoMode = self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="BLUR FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="GRAYSCALE FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(blur_filter)
        
        gauss_filter        = UIWidgets.GaussianBlurWidget(videoMode = self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="GAUSSIAN BLUR FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="GRAYSCALE FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(gauss_filter)

        medianblur_filter   = UIWidgets.MedianBlurWidget(videoMode = self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="MEDIAN BLUR FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="GRAYSCALE FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(medianblur_filter)

        canny_filter        = UIWidgets.CannyWidget(videoMode = self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="CANNY FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="BLUR FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(canny_filter)

        binarythresh_filter = UIWidgets.BinaryThresholdWidget(videoMode = self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="BINARY THRESHOLD FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="BLUR FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(binarythresh_filter)

        dilation_filter     = UIWidgets.DilationWidget(videoMode= self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="DILATION FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="CANNY FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(dilation_filter)

        contour_filter      = UIWidgets.ContourWidget(videoMode= self.__videoMode, availableFilterWidgets=self.__availableFilters, widgetName="CONTOUR FILTER", cvOriginalImage=self.__cvOriginalImage, defaultFilterWidget="DILATION FILTER", parameterChangedCallback=self.parameterChangedCallback)
        self.__availableFilters.append(contour_filter)

        for widget in self.__availableFilters:
            self.filterListBox.addItem(widget.WidgetName)
            if not self.__videoMode: widget.Action()