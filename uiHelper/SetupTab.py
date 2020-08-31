from PyQt5.QtGui import QIntValidator
from utils.AX12 import AX12A
if __name__ =='__main__':
    from RoboKitty import MainWindow
class SetupTab:

    def __init__(self, parent):
        self.parent = parent # type:MainWindow
        self.initSetupTab()
        self.setupValidatorID()

    def updateBaud(self,i):
        self.parent.config.baudIndex = int(i)

    def updatePort(self,port):
        self.parent.config.port = port

    def emergencyStopButtonClicked(self,e):
        try:
            if self.parent.isRoboKittyConnected:
                AX12A.setEnableTorqueGroup(self.parent.ax12aInstances,0)
                AX12A.disconnect()
                self.parent.connectButtonSet.setStyleSheet("")
                self.parent.connectButtonSet.setText("Connect")
                self.parent.isRoboKittyConnected = False
        except:
            pass

    def connectButtonClicked(self,e):
        AX12A.port = self.parent.config.port
        AX12A.baud = self.parent.config.baudRates[self.parent.config.baudIndex][0]

        if not self.parent.isRoboKittyConnected and self.initServo():
            self.parent.isRoboKittyConnected = True
            self.parent.connectButtonSet.setStyleSheet("color :green;")
            self.parent.connectButtonSet.setText("Disconnect")
        elif not self.parent.isRoboKittyConnected:
            self.parent.connectButtonSet.setStyleSheet("color : red;")
            self.parent.connectButtonSet.setChecked(False)
        else:
            if self.parent.isRoboKittyConnected:
                self.emergencyStopButtonClicked(0)

    def initServo(self):
        try:
            AX12A.init()
            if AX12A.connected:
                self.parent.isRoboKittyConnected = True

                self.parent.RearRightShoulder = AX12A(int(self.parent.config.RearRightShoulderID))
                self.parent.RearRightFemer = AX12A(int(self.parent.config.RearRightFemerID))
                self.parent.RearRightLeg = AX12A(int(self.parent.config.RearRightLegID))

                self.parent.ax12aInstances.append(self.parent.RearRightShoulder)
                self.parent.ax12aInstances.append(self.parent.RearRightFemer)
                self.parent.ax12aInstances.append(self.parent.RearRightLeg)

                self.parent.RearLeftShoulder = AX12A(int(self.parent.config.RearLeftShoulderID))
                self.parent.RearLeftFemer = AX12A(int(self.parent.config.RearLeftFemerID))
                self.parent.RearLeftLeg = AX12A(int(self.parent.config.RearLeftLegID))

                self.parent.ax12aInstances.append(self.parent.RearLeftShoulder)
                self.parent.ax12aInstances.append(self.parent.RearLeftFemer)
                self.parent.ax12aInstances.append(self.parent.RearLeftLeg)

                self.parent.FrontLeftShoulder = AX12A(int(self.parent.config.FrontLeftShoulderID))
                self.parent.FrontLeftFemer = AX12A(int(self.parent.config.FrontLeftFemerID))
                self.parent.FrontLeftLeg = AX12A(int(self.parent.config.FrontLeftLegID))
                self.parent.ax12aInstances.append(self.parent.FrontLeftShoulder)
                self.parent.ax12aInstances.append(self.parent.FrontLeftFemer)
                self.parent.ax12aInstances.append(self.parent.FrontLeftLeg)

                self.parent.FrontRightShoulder = AX12A(int(self.parent.config.FrontRightShoulderID))
                self.parent.FrontRightFemer = AX12A(int(self.parent.config.FrontRightFemerID))
                self.parent.FrontRightLeg = AX12A(int(self.parent.config.FrontRightLegID))

                self.parent.ax12aInstances.append(self.parent.FrontRightShoulder)
                self.parent.ax12aInstances.append(self.parent.FrontRightFemer)
                self.parent.ax12aInstances.append(self.parent.FrontRightLeg)

            return True
        except Exception as e:
            print(e)
            return False

    def initSetupTab(self):
        self.parent.baudCBSet.addItems([x[1] for x in self.parent.config.baudRates])
        self.parent.baudCBSet.currentIndexChanged.connect(self.updateBaud)
        self.parent.baudCBSet.setCurrentIndex(self.parent.config.baudIndex)
        self.parent.portLESet.textChanged.connect(self.updatePort)
        self.parent.portLESet.setText(self.parent.config.port)
        self.parent.connectButtonSet.clicked.connect(self.connectButtonClicked)
        self.parent.emergencyStopButtonSet.clicked.connect(self.emergencyStopButtonClicked)

        self.parent.FrontLeftShoulderLESet.setText(str(self.parent.config.FrontLeftShoulderID))
        self.parent.FrontLeftFemerLESet.setText(str(self.parent.config.FrontLeftFemerID))
        self.parent.FrontLeftLegLESet.setText(str(self.parent.config.FrontLeftLegID))

        self.parent.RearLeftShoulderLESet.setText(str(self.parent.config.RearLeftShoulderID))
        self.parent.RearLeftFemerLESet.setText(str(self.parent.config.RearLeftFemerID))
        self.parent.RearLeftLegLESet.setText(str(self.parent.config.RearLeftLegID))

        self.parent.FrontRightShoulderLESet.setText(str(self.parent.config.FrontRightShoulderID))
        self.parent.FrontRightFemerLESet.setText(str(self.parent.config.FrontRightFemerID))
        self.parent.FrontRightLegLESet.setText(str(self.parent.config.FrontRightLegID))

        self.parent.RearRightShoulderLESet.setText(str(self.parent.config.RearRightShoulderID))
        self.parent.RearRightFemerLESet.setText(str(self.parent.config.RearRightFemerID))
        self.parent.RearRightLegLESet.setText(str(self.parent.config.RearRightLegID))

        self.parent.FrontLeftShoulderLESet.textChanged.connect(lambda x: setattr(self.parent.config,"FrontLeftShoulderID",int(x)))
        self.parent.FrontLeftFemerLESet.textChanged.connect(lambda x: setattr(self.parent.config,'FrontLeftFemerID',int(x)))
        self.parent.FrontLeftLegLESet.textChanged.connect(lambda x: setattr(self.parent.config,'FrontLeftLegID',int(x)))

        self.parent.RearLeftShoulderLESet.textChanged.connect(lambda x: setattr(self.parent.config,'RearLeftShoulderID',int(x)))
        self.parent.RearLeftFemerLESet.textChanged.connect(lambda x: setattr(self.parent.config,'RearLeftFemerID',int(x)))
        self.parent.RearLeftLegLESet.textChanged.connect(lambda x: setattr(self.parent.config,'RearLeftLegID',int(x)))

        self.parent.FrontRightShoulderLESet.textChanged.connect(lambda x: setattr(self.parent.config,"FrontRightShoulderID",int(x)))
        self.parent.FrontRightFemerLESet.textChanged.connect(lambda x: setattr(self.parent.config,"FrontRightFemerID",int(x)))
        self.parent.FrontRightLegLESet.textChanged.connect(lambda x: setattr(self.parent.config,"FrontRightLegID",int(x)))

        self.parent.RearRightShoulderLESet.textChanged.connect(lambda x: setattr(self.parent.config,"RearRightShoulderID",int(x)))
        self.parent.RearRightFemerLESet.textChanged.connect(lambda x: setattr(self.parent.config,"RearRightFemerID",int(x)))
        self.parent.RearRightLegLESet.textChanged.connect(lambda x: setattr(self.parent.config,"RearRightLegID",int(x)))

    def setupValidatorID(self):
        self.parent.FrontLeftShoulderLESet.setValidator(QIntValidator())
        self.parent.FrontLeftFemerLESet.setValidator(QIntValidator())
        self.parent.FrontLeftLegLESet.setValidator(QIntValidator())

        self.parent.RearLeftShoulderLESet.setValidator(QIntValidator())
        self.parent.RearLeftFemerLESet.setValidator(QIntValidator())
        self.parent.RearLeftLegLESet.setValidator(QIntValidator())

        self.parent.FrontRightShoulderLESet.setValidator(QIntValidator())
        self.parent.FrontRightFemerLESet.setValidator(QIntValidator())
        self.parent.FrontRightLegLESet.setValidator(QIntValidator())

        self.parent.RearRightShoulderLESet.setValidator(QIntValidator())
        self.parent.RearRightFemerLESet.setValidator(QIntValidator())
        self.parent.RearRightLegLESet.setValidator(QIntValidator())