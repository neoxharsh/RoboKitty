from AX12 import AX12A
import time

def main():
    AX12A.init()
    AX12A.debugEnabled = False
    RearRightSh = AX12A(11)
    RearRightFm = AX12A(10)
    RearRightLe = AX12A(0)

    RearLeftSh = AX12A(8)
    RearLeftFm = AX12A(7)
    RearLeftLe = AX12A(9)

    FrontLeftSh = AX12A(5)
    FrontLeftFm = AX12A(4)
    FrontLeftLe = AX12A(3)

    FrontRightSh = AX12A(2)
    FrontRightFm = AX12A(1)
    FrontRightLe = AX12A(6)

    AX12A.setMaxTorqueGroup(AX12A.allInstances,1023)
    AX12A.setTorqueLimitGroup(AX12A.allInstances,350)
    AX12A.setCWMaxGroup(AX12A.allInstances,0)
    AX12A.setCCWMaxGroup(AX12A.allInstances,1023)
    AX12A.setPositionGroup(AX12A.allInstances,512)
    _cp = FrontRightLe.getPosition()
    while _cp > 512 or _cp < 510:
        _cp = FrontRightLe.getPosition()
    time.sleep(5)

    for motor in AX12A.allInstances:
        _cwLimit = 0
        _ccwLimit = 0
        print("Motor: " + str(motor.id))
        motor.setPosition(1023)
        previousPos = motor.getPosition()
        while True:
            time.sleep(.1)
            curretPos = motor.getPosition()
            if curretPos < previousPos + 2:
                print("max: ", curretPos)
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
                print("min: ", curretPos)
                _cwLimit = curretPos + 5
                break
            else:
                previousPos = curretPos
        motor.setPosition(512)
        _cp = motor.getPosition()
        while _cp > 512 or _cp < 510:
            _cp = motor.getPosition()
        motor.setTorque(0)
        motor.setCWLimit(_cwLimit)
        motor.setCCWLimit(_ccwLimit)
        continue

if __name__ == '__main__':
    main()