from dynamixel_sdk import *


class AX12A:
    debugEnabled = True
    connected = False
    PROTOCOL_VER = 1.0
    port = None
    baud = None

    portHandler = None
    packetHandler = None

    TORQUE_ADDR = [1, 24]
    TORQUE_ENABLE = 1
    TORQUE_DISABLE = 0
    TORQUE_MAX_ADDR = [2, 14]
    TORQUE_LIMIT_ADDR = [2, 34]

    CW_ANGLE_LIMIT_ADDR = [2, 6]
    CCW_ANGLE_LIMIT_ADDR = [2, 8]
    CW_COMPLIANCE_MARGIN_ADDR = [1, 26]
    CCW_COMPLIANCE_MARGIN_ADDR = [1, 27]
    CW_COMPLIANCE_SLOPE_ADDR = [1, 28]
    CCW_COMPLIANCE_SLOPE_ADDR = [1, 29]

    MOVING_SPEED_ADDR = [2, 32]
    IS_MOVING_ADDR = [1,46]

    GOAL_POSITION = [2, 30]
    CURRENT_POSITION = [2, 36]

    LED_ADDR = [1, 25]
    LED_ENABLE = 1
    LED_DISABLE = 0


    groupGoalPosition = GroupSyncWrite(port, portHandler,GOAL_POSITION[1],GOAL_POSITION[0])

    groupMaxTorqueSet = GroupSyncWrite(port,port,TORQUE_MAX_ADDR[1],TORQUE_MAX_ADDR[0])

    def __init__(self,id):
        self.id = id
        if self.__class__.debugEnabled: print("Motor: " + str(self.id) + " Connected")

    @classmethod
    def init(cls):
        if not cls.connected:
            cls.portHandler = PortHandler(cls.port)
            cls.portHandler.setBaudRate(int(cls.baud))
            cls.packetHandler = PacketHandler(cls.PROTOCOL_VER)
            if  cls.portHandler.openPort():
                if cls.debugEnabled: print("Port Connected")
                cls.connected = True


    @classmethod
    def disconnect(cls):
        if cls.connected:
            cls.connected = False
            cls.portHandler.closePort()



    def sendData(self,addrs,data):
        _sender = ""
        if self.__class__.connected:
            if addrs[0] == 1:
                _sender = self.__class__.packetHandler.write1ByteTxRx
            elif addrs[0] == 2:
                _sender = self.__class__.packetHandler.write2ByteTxRx
            elif addrs[0] == 3:
                _sender = self.__class__.packetHandler.write4ByteTxRx

            _comResult, _error = _sender(self.__class__.portHandler,self.id,addrs[1],data)

            if _comResult != COMM_SUCCESS:
                if self.__class__.debugEnabled: print(self.__class__.packetHandler.getTxRxResult(_comResult))

            if _error != 0:
                if self.__class__.debugEnabled: print(self.__class__.packetHandler.getRxPacketError(_error))

    def getData(self,addrs):
        _reciever = ""
        if self.__class__.connected:
            if addrs[0] == 1:
                _reciever = self.__class__.packetHandler.read1ByteTxRx
            elif addrs[0] == 2:
                _reciever = self.__class__.packetHandler.read2ByteTxRx
            elif addrs[0] == 3:
                _reciever = self.__class__.packetHandler.read4ByteTxRx

            _result, _comResult, _error = _reciever(self.__class__.portHandler,self.id, addrs[1])

            if _comResult != COMM_SUCCESS:
                if self.__class__.debugEnabled: print(self.__class__.packetHandler.getTxRxResult(_comResult))

            if _error != 0:
                if self.__class__.debugEnabled: print(self.__class__.packetHandler.getRxPacketError(_error))
            else:
                return _result

    def setTorque(self,torqueEnableOrDisable):
        self.sendData(self.TORQUE_ADDR,torqueEnableOrDisable)

    def setMaxTorque(self,value):
        self.sendData(self.TORQUE_MAX_ADDR,value)

    def setTorqueLimit(self,value):
        self.sendData(self.TORQUE_LIMIT_ADDR,value)

    def setPosition(self,position):
        self.sendData(self.GOAL_POSITION,position)

    def getPosition(self):
        return self.getData(self.CURRENT_POSITION)

    def isMoving(self):
        return self.getData(self.IS_MOVING_ADDR)

    def setLED(self,onOROff):
        self.sendData(self.LED_ADDR,onOROff)

    def getCWLimit(self):
        return self.getData(self.CW_ANGLE_LIMIT_ADDR)

    def getCCWLimit(self):
        return self.getData(self.CCW_ANGLE_LIMIT_ADDR)

    def setCWLimit(self,_value):
        self.sendData(self.CW_ANGLE_LIMIT_ADDR,_value)

    def setCCWLimit(self,_value):
        self.sendData(self.CCW_ANGLE_LIMIT_ADDR, _value)

    @classmethod
    def setPositionGroup(cls, motors: list, value = None):
        groupPositionSet = GroupSyncWrite(cls.portHandler,cls.packetHandler,cls.GOAL_POSITION[1],cls.GOAL_POSITION[0])
        if value == None:
            for motor in motors:
                _value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                          DXL_HIBYTE(DXL_LOWORD(motor[1])),
                        ]
                if cls.debugEnabled:
                    print("Position Set: "+ str(motor[0].id) + " " + str(groupPositionSet.addParam(motor[0].id,_value)))
                else:
                    groupPositionSet.addParam(motor[0].id,_value)
        else:
            _value = [DXL_LOBYTE(DXL_LOWORD(value)),
                      DXL_HIBYTE(DXL_LOWORD(value)),

                      ]
            for motor in motors:
                if cls.debugEnabled:
                    print("Position Set: "+ str(motor.id) + " " + str(groupPositionSet.addParam(motor.id,_value)))
                else:
                    groupPositionSet.addParam(motor.id,_value)

        _result = groupPositionSet.txPacket()
        if _result != COMM_SUCCESS:
            print(cls.packetHandler.getTxRxResult(_result))
        groupPositionSet.clearParam()

    @classmethod
    def setPositionTorqueSpeedGroup(cls, motors: list):
        groupPositionSet = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.GOAL_POSITION[1],
                                          cls.GOAL_POSITION[0])
        groupSpeed = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.MOVING_SPEED_ADDR[1], cls.MOVING_SPEED_ADDR[0])
        groupMaxTorqueSet = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.TORQUE_MAX_ADDR[1],
                                           cls.TORQUE_MAX_ADDR[0])
        #Speed
        for motor in motors:
            _value = [DXL_LOBYTE(DXL_LOWORD(motor[3])),
                      DXL_HIBYTE(DXL_LOWORD(motor[3])),
                     ]
            if cls.debugEnabled:
                print("Position Set: "+ str(motor[0].id) + " " + str(groupSpeed.addParam(motor[0].id, _value)))
            else:
                groupSpeed.addParam(motor[0].id, _value)
        groupSpeed.txPacket()
        groupSpeed.clearParam()

        #Torque
        for motor in motors:
            _value = [DXL_LOBYTE(DXL_LOWORD(motor[2])),
                      DXL_HIBYTE(DXL_LOWORD(motor[2])),
                      ]
            if cls.debugEnabled:
                print("Max Torque Set: "+ str(motor[0].id) + " "+ str(groupMaxTorqueSet.addParam(motor[0].id, _value)))
            else:
                groupMaxTorqueSet.addParam(motor[0].id, _value)
        groupMaxTorqueSet.txPacket()
        groupMaxTorqueSet.clearParam()

        #Position
        for motor in motors:
            _value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                      DXL_HIBYTE(DXL_LOWORD(motor[1])),
                     ]
            if cls.debugEnabled:
                print("Position Set: "+ str(motor[0].id) + " " + str(groupPositionSet.addParam(motor[0].id, _value)))
            else:
                groupPositionSet.addParam(motor[0].id, _value)
        groupPositionSet.txPacket()
        groupPositionSet.clearParam()

    @classmethod
    def setSpeedGroup(cls, motors: list, value=None):
        groupSpeed = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.MOVING_SPEED_ADDR[1], cls.MOVING_SPEED_ADDR[0])
        if value == None:
            for motor in motors:
                _value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                          DXL_HIBYTE(DXL_LOWORD(motor[1])),
                        ]
                if cls.debugEnabled:
                    print("Speed Set: "+ str(motor[0].id) + " " + str(groupSpeed.addParam(motor[0].id,_value)))
                else:
                    groupSpeed.addParam(motor[0].id, _value)
        else:
            _value = [DXL_LOBYTE(DXL_LOWORD(value)),
                      DXL_HIBYTE(DXL_LOWORD(value)),
                     ]
            for motor in motors:
                if cls.debugEnabled:
                    print("Speed Set: "+ str(motor.id) + " " + str(groupSpeed.addParam(motor.id, _value)))
                else:
                    groupSpeed.addParam(motor.id, _value)
        groupSpeed.txPacket()
        groupSpeed.clearParam()

    @classmethod
    def setLEDGroup(cls, motors: list, value=None):
        groupLEDSet = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.LED_ADDR[1], cls.LED_ADDR[0])

        if value == None:
            for motor in motors:
                if cls.debugEnabled:
                    print("LED Set: "+ str(motor[0].id) + " " + str(groupLEDSet.addParam(motor[0].id, [motor[1]])))
                else:
                    groupLEDSet.addParam(motor[0].id, [motor[1]])
        else:
            for motor in motors:
                if cls.debugEnabled:
                    print("LED Set: "+ str(motor.id) + " " + str(groupLEDSet.addParam(motor.id, [value])))
                else:
                    groupLEDSet.addParam(motor.id, [value])
        groupLEDSet.txPacket()
        groupLEDSet.clearParam()

    @classmethod
    def setMaxTorqueGroup(cls, motors: list, maxTorque=None):
        groupMaxTorqueSet = GroupSyncWrite(cls.portHandler,cls.packetHandler,cls.TORQUE_MAX_ADDR[1],cls.TORQUE_MAX_ADDR[0])
        if maxTorque == None:
            for motor in motors:
                _value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                          DXL_HIBYTE(DXL_LOWORD(motor[1]))]
                if cls.debugEnabled:
                    print("Max Torque Set: "+ str(motor[0].id) + " " + str(groupMaxTorqueSet.addParam(motor[0].id,_value)))
                else:
                    groupMaxTorqueSet.addParam(motor[0].id,_value)
        else:
            _value = [DXL_LOBYTE(DXL_LOWORD(maxTorque)),
                      DXL_HIBYTE(DXL_LOWORD(maxTorque))]
            for motor in motors:
                if cls.debugEnabled:
                    print("Max Torque Set: "+ str(motor.id) + " " + str(groupMaxTorqueSet.addParam(motor.id, _value)))
                else:
                    groupMaxTorqueSet.addParam(motor.id, _value)
        groupMaxTorqueSet.txPacket()
        groupMaxTorqueSet.clearParam()

    @classmethod
    def setTorqueLimitGroup(cls, motors: list, maxTorque=None):
        groupMaxTorqueSet = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.TORQUE_LIMIT_ADDR[1],
                                           cls.TORQUE_LIMIT_ADDR[0])
        if maxTorque == None:
            for motor in motors:
                _value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                          DXL_HIBYTE(DXL_LOWORD(motor[1]))]
                if cls.debugEnabled:
                    print("Max Torque Set: " + str(motor[0].id) + " " + str(
                        groupMaxTorqueSet.addParam(motor[0].id, _value)))
                else:
                    groupMaxTorqueSet.addParam(motor[0].id, _value)
        else:
            _value = [DXL_LOBYTE(DXL_LOWORD(maxTorque)),
                      DXL_HIBYTE(DXL_LOWORD(maxTorque))]
            for motor in motors:
                if cls.debugEnabled:
                    print("Max Torque Set: " + str(motor.id) + " " + str(
                        groupMaxTorqueSet.addParam(motor.id, _value)))
                else:
                    groupMaxTorqueSet.addParam(motor.id, _value)
        groupMaxTorqueSet.txPacket()
        groupMaxTorqueSet.clearParam()

    @classmethod
    def setEnableTorqueGroup(cls, motors: list, enable=None):
        groupEnableTorqueSet = GroupSyncWrite(cls.portHandler,cls.packetHandler,cls.TORQUE_ADDR[1],cls.TORQUE_ADDR[0])
        if enable == None:
            for motor in motors:
                if cls.debugEnabled:
                    print("Torque Set: "+ str(motor[0].id) + " " + str(groupEnableTorqueSet.addParam(motor[0].id, [motor[1]])))
                else:
                    groupEnableTorqueSet.addParam(motor[0].id,[motor[1]])
        else:
            for motor in motors:
                if cls.debugEnabled:
                    print("Torque Set: "+ str(motor.id) + " " + str(groupEnableTorqueSet.addParam(motor.id, [enable])))
                else:
                    groupEnableTorqueSet.addParam(motor.id,[enable])
        groupEnableTorqueSet.txPacket()
        groupEnableTorqueSet.clearParam()

    @classmethod
    def setCWMaxGroup(cls, motors: list, value=None):
        groupEnableTorqueSet = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.CW_ANGLE_LIMIT_ADDR[1],
                                              cls.CW_ANGLE_LIMIT_ADDR[0])
        if value == None:
            for motor in motors:
                value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                         DXL_HIBYTE(DXL_LOWORD(motor[1]))]
                if cls.debugEnabled:
                    print("CW Set: " + str(motor[0].id) + " " + str(
                        groupEnableTorqueSet.addParam(motor[0].id, value)))
                else:
                    groupEnableTorqueSet.addParam(motor[0].id, value)
        else:
            value = [DXL_LOBYTE(DXL_LOWORD(value)),
                     DXL_HIBYTE(DXL_LOWORD(value))]
            for motor in motors:
                if cls.debugEnabled:
                    print("CW Set: " + str(motor.id) + " " + str(groupEnableTorqueSet.addParam(motor.id, value)))
                else:
                    groupEnableTorqueSet.addParam(motor.id, value)
        groupEnableTorqueSet.txPacket()
        groupEnableTorqueSet.clearParam()

    @classmethod
    def setCCWMaxGroup(cls, motors: list, value=None):
        groupEnableTorqueSet = GroupSyncWrite(cls.portHandler, cls.packetHandler, cls.CCW_ANGLE_LIMIT_ADDR[1],
                                              cls.CCW_ANGLE_LIMIT_ADDR[0])
        if value == None:
            for motor in motors:
                value = [DXL_LOBYTE(DXL_LOWORD(motor[1])),
                         DXL_HIBYTE(DXL_LOWORD(motor[1]))]
                if cls.debugEnabled:
                    print("CW Set: " + str(motor[0].id) + " " + str(
                        groupEnableTorqueSet.addParam(motor[0].id, value)))
                else:
                    groupEnableTorqueSet.addParam(motor[0].id, value)
        else:
            value = [DXL_LOBYTE(DXL_LOWORD(value)),
                     DXL_HIBYTE(DXL_LOWORD(value))]
            for motor in motors:
                if cls.debugEnabled:
                    print("CW Set: " + str(motor.id) + " " + str(groupEnableTorqueSet.addParam(motor.id, value)))
                else:
                    groupEnableTorqueSet.addParam(motor.id, value)
        groupEnableTorqueSet.txPacket()
        groupEnableTorqueSet.clearParam()