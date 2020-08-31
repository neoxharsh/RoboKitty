from PyQt5.QtWidgets import QLabel,QSlider
from PyQt5 import QtGui

class CustomQLabel(QLabel):

    def __init__(self,parent):
        super(CustomQLabel,self).__init__()
        self.slider = None # type:QSlider
        self.parent = None
        self.column = None
        self.isToggled = False
        self.setStyleSheet('color:red;')

    def linkParent(self,parent):
        self.parent = parent

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.parent.inManualRecordMode:
            if self.isToggled:
                self.isToggled = False
                self.slider.setEnabled(False)
                self.setStyleSheet('color:red;')
                self.slider.setValue(self.slider.minimum())
                self.parent.motionDataModel.setCellData(self.parent.currentRowIndex,self.column,None)
            else:
                self.isToggled = True
                self.slider.setEnabled(True)
                self.setStyleSheet('color:green;')

    def setSliderAndColumn(self,slider,column):
        self.slider = slider
        self.column = column