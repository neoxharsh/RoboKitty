from utils.AX12 import AX12A
if __name__ =='__main__':
    from RoboKitty import MainWindow


class ManualControlTab:

    def __init__(self,parent):
        self.parent = parent # type: MainWindow
        self.initTab()

    def motorsEnableButtonClicked(self,e):
        if not self.parent.areMotorsEnabled and self.parent.isRoboKittyConnected and self:
            AX12A.setEnableTorqueGroup(self.parent.ax12aInstances,1)
            self.parent.motorsEnableButtonMC.setText("Disable Motors")
            self.setSlidersRange()
            self.parent.areMotorsEnabled = True
        else:
            if self.parent.isRoboKittyConnected:
                AX12A.setEnableTorqueGroup(self.parent.ax12aInstances,0)
            self.parent.motorsEnableButtonMC.setChecked(False)
            self.parent.motorsEnableButtonMC.setText("Enable Motors")
            self.parent.areMotorsEnabled = False

    def setSlidersRange(self):
        self.parent.rearLeftShoulderSliderMC.setMaximum(self.parent.RearLeftShoulder.getCCWLimit())
        self.parent.rearLeftShoulderSliderMC.setMinimum(self.parent.RearLeftShoulder.getCWLimit())
        self.parent.rearLeftShoulderSliderMC.setValue(self.parent.RearLeftShoulder.getPosition())

        self.parent.frontLeftShoulderSliderMC.setMaximum(self.parent.FrontLeftShoulder.getCCWLimit())
        self.parent.frontLeftShoulderSliderMC.setMinimum(self.parent.FrontLeftShoulder.getCWLimit())
        self.parent.frontLeftShoulderSliderMC.setValue(self.parent.FrontLeftShoulder.getPosition())

        self.parent.rearRightShoulderSliderMC.setMaximum(self.parent.RearRightShoulder.getCCWLimit())
        self.parent.rearRightShoulderSliderMC.setMinimum(self.parent.RearRightShoulder.getCWLimit())
        self.parent.rearRightShoulderSliderMC.setValue(self.parent.RearRightShoulder.getPosition())

        self.parent.frontRightShoulderSliderMC.setMaximum(self.parent.FrontRightShoulder.getCCWLimit())
        self.parent.frontRightShoulderSliderMC.setMinimum(self.parent.FrontRightShoulder.getCWLimit())
        self.parent.frontRightShoulderSliderMC.setValue(self.parent.FrontRightShoulder.getPosition())



        self.parent.rearLeftFemerSliderMC.setMaximum(self.parent.RearLeftFemur.getCCWLimit())
        self.parent.rearLeftFemerSliderMC.setMinimum(self.parent.RearLeftFemur.getCWLimit())
        self.parent.rearLeftFemerSliderMC.setValue(self.parent.RearLeftFemur.getPosition())

        self.parent.frontLeftFemerSliderMC.setMaximum(self.parent.FrontLeftFemur.getCCWLimit())
        self.parent.frontLeftFemerSliderMC.setMinimum(self.parent.FrontLeftFemur.getCWLimit())
        self.parent.frontLeftFemerSliderMC.setValue(self.parent.FrontLeftFemur.getPosition())

        self.parent.rearRightFemerSliderMC.setMaximum(self.parent.RearRightFemur.getCCWLimit())
        self.parent.rearRightFemerSliderMC.setMinimum(self.parent.RearRightFemur.getCWLimit())
        self.parent.rearRightFemerSliderMC.setValue(self.parent.RearRightFemur.getPosition())

        self.parent.frontRightFemerSliderMC.setMaximum(self.parent.FrontRightFemur.getCCWLimit())
        self.parent.frontRightFemerSliderMC.setMinimum(self.parent.FrontRightFemur.getCWLimit())
        self.parent.frontRightFemerSliderMC.setValue(self.parent.FrontRightFemur.getPosition())


        self.parent.rearLeftLegSliderMC.setMaximum(self.parent.RearLeftLeg.getCCWLimit())
        self.parent.rearLeftLegSliderMC.setMinimum(self.parent.RearLeftLeg.getCWLimit())
        self.parent.rearLeftLegSliderMC.setValue(self.parent.RearLeftLeg.getPosition())

        self.parent.frontLeftLegSliderMC.setMaximum(self.parent.FrontLeftLeg.getCCWLimit())
        self.parent.frontLeftLegSliderMC.setMinimum(self.parent.FrontLeftLeg.getCWLimit())
        self.parent.frontLeftLegSliderMC.setValue(self.parent.FrontLeftLeg.getPosition())

        self.parent.rearRightLegSliderMC.setMaximum(self.parent.RearRightLeg.getCCWLimit())
        self.parent.rearRightLegSliderMC.setMinimum(self.parent.RearRightLeg.getCWLimit())
        self.parent.rearRightLegSliderMC.setValue(self.parent.RearRightLeg.getPosition())

        self.parent.frontRightLegSliderMC.setMaximum(self.parent.FrontRightLeg.getCCWLimit())
        self.parent.frontRightLegSliderMC.setMinimum(self.parent.FrontRightLeg.getCWLimit())
        self.parent.frontRightLegSliderMC.setValue(self.parent.FrontRightLeg.getPosition())

        self.parent.rearLeftShoulderSliderMC.valueChanged.connect(
            lambda value: self.parent.RearLeftShoulder.setPosition(value))
        self.parent.rearLeftFemerSliderMC.valueChanged.connect(
            lambda value: self.parent.RearLeftFemur.setPosition(value))
        self.parent.rearLeftLegSliderMC.valueChanged.connect(lambda value: self.parent.RearLeftLeg.setPosition(value))

        self.parent.rearRightShoulderSliderMC.valueChanged.connect(
            lambda value: self.parent.RearRightShoulder.setPosition(value))
        self.parent.rearRightFemerSliderMC.valueChanged.connect(
            lambda value: self.parent.RearRightFemur.setPosition(value))
        self.parent.rearRightLegSliderMC.valueChanged.connect(lambda value: self.parent.RearRightLeg.setPosition(value))

        self.parent.frontLeftShoulderSliderMC.valueChanged.connect(
            lambda value: self.parent.FrontLeftShoulder.setPosition(value))
        self.parent.frontLeftFemerSliderMC.valueChanged.connect(
            lambda value: self.parent.FrontLeftFemur.setPosition(value))
        self.parent.frontLeftLegSliderMC.valueChanged.connect(lambda value: self.parent.FrontLeftLeg.setPosition(value))

        self.parent.frontRightShoulderSliderMC.valueChanged.connect(
            lambda value: self.parent.FrontRightShoulder.setPosition(value))
        self.parent.frontRightFemerSliderMC.valueChanged.connect(
            lambda value: self.parent.FrontRightFemur.setPosition(value))
        self.parent.frontRightLegSliderMC.valueChanged.connect(
            lambda value: self.parent.FrontRightLeg.setPosition(value))

    def initTab(self):
        self.parent.motorsEnableButtonMC.clicked.connect(self.motorsEnableButtonClicked)