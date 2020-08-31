from PyQt5.QtWidgets import QSlider
from PyQt5 import QtGui


class CustomQSlider(QSlider):

    def __init__(self,*args, **kwargs):
        super(CustomQSlider,self).__init__(*args, **kwargs)
        self.slider = None # type:QSlider
        self.parent = None
        self.motor = None
        self.valueChanged.connect(self.onValueChanged)

    def linkParent(self,parent):
        self.parent = parent

    def linkMotor(self,motor):
        self.motor = motor

    def onValueChanged(self,v):
        if self.parent.inManualRecordMode:
            self.motor.setPosition(v)
