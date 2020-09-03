from PyQt5.QtWidgets import QSlider
from PyQt5 import QtGui


class CustomQSlider(QSlider):
    allInstances = []
    def __init__(self,*args, **kwargs):
        super(CustomQSlider,self).__init__(*args, **kwargs)
        self.slider = None # type:QSlider
        self.parent = None
        self.motor = None
        self.valueChanged.connect(self.onValueChanged)
        self.column = None
        self.allInstances.append(self)

    def setParentAndColumn(self,parent,column):
        self.parent = parent
        self.column = column

    def setMotor(self,motor):
        self.motor = motor

    def onValueChanged(self,v):
        if self.parent.inManualRecordMode:
            self.parent.motionDataModel.setCellData(self.parent.currentRowIndex, self.column, v)
            self.motor.setTorque(True)
            self.motor.setPosition(v)