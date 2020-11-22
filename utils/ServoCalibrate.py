from utils.AX12 import AX12A
import time

class ServoCalibrate:

    def __init__(self,parent):
        self.parent = parent
        self.isConnected = False
        self._max = 515
        self._min = 502


    def centerServo(self):
        AX12A.setMaxTorqueGroup(self.parent.ax12aInstances, 1023)
        AX12A.setTorqueLimitGroup(self.parent.ax12aInstances, 350)
        AX12A.setPositionGroup(self.parent.ax12aInstances, 512)
        AX12A.setCWMaxGroup(self.parent.ax12aInstances,0)
        AX12A.setCCWMaxGroup(self.parent.ax12aInstances,1023)
        _max = self._max
        _min = self._min
        _cp = self.parent.FrontRightShoulder.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.FrontRightShoulder.getPosition()

        _cp = self.parent.FrontRightFemur.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.FrontRightFemur.getPosition()

        _cp = self.parent.FrontRightLeg.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.FrontRightLeg.getPosition()

        _cp = self.parent.RearRightShoulder.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.RearRightShoulder.getPosition()

        _cp = self.parent.RearRightFemur.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.RearRightFemur.getPosition()

        _cp = self.parent.RearRightLeg.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.RearRightLeg.getPosition()

        _cp = self.parent.FrontLeftShoulder.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.FrontLeftShoulder.getPosition()

        _cp = self.parent.FrontLeftFemur.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.FrontLeftFemur.getPosition()

        _cp = self.parent.FrontLeftLeg.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.FrontLeftLeg.getPosition()

        _cp = self.parent.RearLeftShoulder.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.RearLeftShoulder.getPosition()

        _cp = self.parent.RearLeftFemur.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.RearLeftFemur.getPosition()

        _cp = self.parent.RearLeftLeg.getPosition()
        while _cp > _max or _cp < _min:
            _cp = self.parent.RearLeftLeg.getPosition()
        print("Centering Done")

    def calibrateServo(self,motor):
        _cwLimit = 0
        _ccwLimit = 0
        motor.setPosition(1023)
        previousPos = motor.getPosition()
        while True:
            time.sleep(.1)
            curretPos = motor.getPosition()
            if curretPos < previousPos + 2:
                _ccwLimit = curretPos - 5
                break
            else:
                previousPos = curretPos

        motor.setPosition(0)
        previousPos = motor.getPosition()
        while True:
            time.sleep(.1)
            curretPos = motor.getPosition()
            if curretPos > previousPos - 2:
                _cwLimit = curretPos + 5
                break
            else:
                previousPos = curretPos
        motor.setPosition(512)
        _cp = motor.getPosition()
        while _cp > self._max or _cp < self._min:
            _cp = motor.getPosition()
        motor.setTorque(0)
        motor.setCWLimit(_cwLimit)
        motor.setCCWLimit(_ccwLimit)
        return _cwLimit,_ccwLimit