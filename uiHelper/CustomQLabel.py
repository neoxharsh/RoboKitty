from PyQt5.QtWidgets import QLabel,QSlider
from PyQt5 import QtGui

class CustomQLabel(QLabel):
    allInstances =[]
    def __init__(self,parent):
        super(CustomQLabel,self).__init__()
        self.slider = None # type:QSlider
        self.parent = None
        self.column = None
        self.isToggled = False
        self.motor = None
        self.setStyleSheet('color:red;')
        self.allInstances.append(self)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.parent.inManualRecordMode:
            if self.isToggled:
                self.isToggled = False
                self.slider.setEnabled(False)
                self.setStyleSheet('color:red;')
                self.parent.motionDataModel.setCellData(self.parent.currentRowIndex,self.column,None)
            else:
                self.isToggled = True
                self.slider.setEnabled(True)
                self.slider.setValue(self.motor.getPosition())
                self.setStyleSheet('color:green;')

    def setMotor(self,motor):
        self.motor = motor

    def setParentSliderColumn(self,parent,slider,column):
        self.parent = parent
        self.slider = slider
        self.column = column

    @classmethod
    def disableAll(cls):
        for i in cls.allInstances:
            i.setStyleSheet('color:red;')
            i.isToggled = False
            i.slider.setEnabled(False)