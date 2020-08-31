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
    AX12A.setEnableTorqueGroup(AX12A.allInstances,1)
    AX12A.setTorqueLimitGroup(AX12A.allInstances,1023)
    AX12A.setSpeedGroup(AX12A.allInstances, 100)


    # AX12A.setPositionGroup([RearRightSh,RearLeftSh,FrontLeftSh,FrontRightSh],512)

    #Standing Pose
    FrontLeftLe.setPosition(670)
    time.sleep(.5)
    FrontRightSh.setPosition(480)
    time.sleep(.5)
    FrontLeftSh.setPosition(530)
    time.sleep(.5)
    AX12A.setPositionGroup([
        [FrontRightLe,200],
        [FrontLeftLe,800]]
    )
    time.sleep(.5)
    RearLeftLe.setPosition(871)
    time.sleep(.5)
    RearRightSh.setPosition(530)
    time.sleep(.5)
    RearLeftSh.setPosition(480)
    time.sleep(.5)
    AX12A.setPositionGroup([
        [RearRightLe, 200],
        [RearLeftLe, 800]]
    )

if __name__ == '__main__':
    main()

