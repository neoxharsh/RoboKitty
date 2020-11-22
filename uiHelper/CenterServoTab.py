from utils.AX12 import AX12A
from PyQt5.QtWidgets import QLineEdit,QLabel
if __name__ =='__main__':
    from RoboKitty import MainWindow

class CenterServoTab:

    def __init__(self,parent) -> None:
         self.parent = parent # type:MainWindow
         self.parent.servoNameLabelCS.setText("Servo Name: ")
         self.parent.servoIDLabelCS.setText("Servo ID:   ")
         self.currentServoIndex = 0
         self.init()
    
    def onTabActivate(self):
        if self.parent.isRoboKittyConnected:
            self.parent.servoNameLabelCS.setText("Servo Name: " + self.parent.ax12aInstances[self.currentServoIndex].name)
            self.parent.servoIDLabelCS.setText("Servo ID:   " + str(self.parent.ax12aInstances[self.currentServoIndex].id))
            self.parent.ax12aInstances[self.currentServoIndex].setLED(True)


    def init(self):
        self.parent.centerServoButtonCS.clicked.connect(self.onCenterButtonClicked)
        self.parent.nextButtonCS.clicked.connect(self.onNextButtonClicked)
        self.parent.previousButtonCS.clicked.connect(self.onPreviousButtonClicked)

    def onCenterButtonClicked(self,e):
        if self.parent.isRoboKittyConnected:
            currentServo = self.parent.ax12aInstances[self.currentServoIndex] # type:AX12A
            currentServo.setMaxTorque(1023)
            currentServo.setTorqueLimit(1023)
            currentServo.setPosition(512)
            

    def onNextButtonClicked(self,e):
        if self.parent.isRoboKittyConnected:
            if self.currentServoIndex <11:
                self.currentServoIndex+= 1
                self.parent.ax12aInstances[self.currentServoIndex].setLED(True)
                self.parent.ax12aInstances[self.currentServoIndex-1].setLED(False)
            self.parent.servoNameLabelCS.setText("Servo Name: " + self.parent.ax12aInstances[self.currentServoIndex].name)
            self.parent.servoIDLabelCS.setText("Servo ID:   " + str(self.parent.ax12aInstances[self.currentServoIndex].id))

        

    def onPreviousButtonClicked(self,e):
        if self.parent.isRoboKittyConnected:
            if self.currentServoIndex >0:
                self.currentServoIndex-= 1
                self.parent.ax12aInstances[self.currentServoIndex].setLED(True)
                self.parent.ax12aInstances[self.currentServoIndex+1].setLED(False)
            self.parent.servoNameLabelCS.setText("Servo Name: " + self.parent.ax12aInstances[self.currentServoIndex].name)
            self.parent.servoIDLabelCS.setText("Servo ID:   " + str(self.parent.ax12aInstances[self.currentServoIndex].id))
            self.parent.ax12aInstances[self.currentServoIndex].setLED(True)