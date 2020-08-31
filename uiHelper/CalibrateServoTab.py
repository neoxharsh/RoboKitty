
from utils.ServoCalibrate import ServoCalibrate
from PyQt5.QtCore import pyqtSignal,QThread
from utils.AX12 import AX12A
from PyQt5.QtWidgets import QLineEdit,QLabel
if __name__ =='__main__':
    from RoboKitty import MainWindow

class CalibrateServoTab:

    def __init__(self,parent):
        self.parent = parent # type:MainWindow
        self.isCalibrating = False
        self.calibratedBefore = False
        self.servoCalibrate = ServoCalibrate(self.parent)
        self.servoCalibrateThread = None
        self.parent.calibrateServoButtonCS.clicked.connect(self.calibrateServoButtonClicked)
        self.parent.stopCalibrationButtonCS.clicked.connect(self.stopCalibration)


    def calibrateServoButtonClicked(self,e):
        if self.parent.isRoboKittyConnected:
            self.parent.connectButtonSet.setEnabled(False)
            self.parent.calibrateServoButtonCS.setEnabled(False)
            self.parent.calibrateServoButtonCS.setText("Centering...")
            _servoCentered = ServoCenterClass(self)
            _servoCentered.centeredSignal.connect(lambda :self.calibrateServo())
            self.isCalibrating = True
            _servoCentered.start()
        else:
            self.parent.calibrateServoButtonCS.setChecked(False)


    def calibrateServo(self):
        self.parent.calibrateServoButtonCS.setText("Calibrating..")
        if self.parent.isRoboKittyConnected:
            motors = [
                [self.parent.FrontLeftShoulder, self.parent.FrontLeftShoulderLESet, self.parent.frontLeftShoulderLabelCS],
                [self.parent.FrontLeftFemer, self.parent.FrontLeftFemerLESet, self.parent.frontLeftFemerLabelCS],
                [self.parent.FrontLeftLeg, self.parent.FrontLeftLegLESet, self.parent.frontLeftLegLabelCS],

                [self.parent.FrontRightShoulder, self.parent.FrontRightShoulderLESet, self.parent.frontRightShoulderLabelCS],
                [self.parent.FrontRightFemer, self.parent.FrontRightFemerLESet, self.parent.frontRightFemerLabelCS],
                [self.parent.FrontRightLeg, self.parent.FrontRightLegLESet, self.parent.frontRightLegLabelCS],

                [self.parent.RearLeftShoulder, self.parent.RearLeftShoulderLESet, self.parent.rearLeftShoulderLabelCS],
                [self.parent.RearLeftFemer, self.parent.RearLeftFemerLESet, self.parent.rearLeftFemerLabelCS],
                [self.parent.RearLeftLeg, self.parent.RearLeftLegLESet, self.parent.rearLeftLegLabelCS],

                [self.parent.RearRightShoulder, self.parent.RearRightShoulderLESet, self.parent.rearRightShoulderCS],
                [self.parent.RearRightFemer, self.parent.RearRightFemerLESet, self.parent.rearRightFemerLabelCS],
                [self.parent.RearRightLeg, self.parent.RearRightLegLESet, self.parent.rearRightLegLabelCS]
            ]
            self.servoCalibrateThread = ServoCalibrateClass(self,motors)
            self.servoCalibrateThread.servoIDSignal.connect(self.updateID)
            self.servoCalibrateThread.calibrationFinishedSignal.connect(self.calibrationFinished)
            self.servoCalibrateThread.servoDataSignal.connect(self.servoDataUpdate)
            self.servoCalibrateThread.start()

        else:
            self.parent.calibrateServoButtonCS.setChecked(False)

    def updateID(self,id,field):
        if not self.calibratedBefore:
            field.setText(f"{field.text():21s} - ID: {id:03d}")
        else:
            field.setText(f"{field.text()[:21]:21s} - ID: {id:03d}")

    def calibrationFinished(self):
        self.parent.calibrateServoButtonCS.setChecked(False)
        self.parent.calibrateServoButtonCS.setText("Calibrate Again")
        self.parent.calibrateServoButtonCS.setEnabled(True)
        self.parent.stopCalibrationButtonCS.setEnabled(False)
        self.parent.connectButtonSet.setEnabled(True)
        self.isCalibrating = False
        self.calibratedBefore = True

    def servoDataUpdate(self,cw,ccw,field):
        field.setText(f"{field.text()[:31]}, CW: {cw:04d}, CCW: {ccw:04d}")

    def stopCalibration(self,e):
        self.servoCalibrateThread.running = False
        self.parent.stopCalibrationButtonCS.setEnabled(False)

class ServoCalibrateClass(QThread):
    servoIDSignal = pyqtSignal(int,QLineEdit)
    calibrationFinishedSignal = pyqtSignal()
    servoDataSignal = pyqtSignal(int,int,QLabel)

    def __init__(self,parent:CalibrateServoTab,motors):
        super(ServoCalibrateClass, self).__init__(parent.parent)
        self.parent = parent

        self.parent.parent.stopCalibrationButtonCS.setEnabled(True)
        self.motors = motors
        self.running = True

    def run(self) -> None:
        for motor in self.motors:
            if not self.running:
                break
            if not motor[1].text() == "":
                motor[0] = AX12A(int(motor[1].text()))
            self.servoIDSignal.emit(motor[0].id,motor[2])
            cw,ccw = self.parent.servoCalibrate.calibrateServo(motor[0])
            self.servoDataSignal.emit(cw,ccw,motor[2])
        self.parent.calibratedBefore = True
        self.calibrationFinishedSignal.emit()


class ServoCenterClass(QThread):
    centeredSignal = pyqtSignal()
    def __init__(self,parent:CalibrateServoTab):
        super(ServoCenterClass, self).__init__(parent.parent)
        self.parent = parent

    def run(self) -> None:
        self.parent.servoCalibrate.centerServo()
        self.centeredSignal.emit()