from PyQt5.QtWidgets import QTabWidget,QApplication
from PyQt5.QtGui import QMouseEvent,QIntValidator,QKeyEvent,QCloseEvent,QResizeEvent
import sys,pickle
from utils.ConfigFile import Config
from motionRecordUI import Ui_MainWindow
from utils.AX12 import AX12A

from uiHelper.CalibrateServoTab import CalibrateServoTab
from uiHelper.SetupTab import SetupTab
from uiHelper.ManualControlTab import ManualControlTab
from uiHelper.MotionRecorderTab import MotionRecorderTab


class MainWindow(QTabWidget,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.config = Config()
        try:
            self.config = pickle.load(open('config.pkl','rb'))

        except:
            print("error opening Config File")
        self.isRoboKittyConnected = False
        self.areMotorsEnabled = False

        self.RearRightShoulder = None # type:AX12A
        self.RearRightFemer = None # type:AX12A
        self.RearRightLeg = None # type:AX12A

        self.RearLeftShoulder = None # type:AX12A
        self.RearLeftFemer = None # type:AX12A
        self.RearLeftLeg = None # type:AX12A

        self.FrontLeftShoulder = None # type:AX12A
        self.FrontLeftFemer = None # type:AX12A
        self.FrontLeftLeg = None # type:AX12A

        self.FrontRightShoulder = None # type:AX12A
        self.FrontRightFemer = None # type:AX12A
        self.FrontRightLeg = None # type:AX12A

        self.ax12aInstances = []
        AX12A.debugEnabled = False
        self.setupUi(self)
        # self.setFixedSize(890,400)
        self.setCurrentIndex(1)
        self.init()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        pass

    def resizeEvent(self, a0: QResizeEvent) -> None:
        QTabWidget.resizeEvent(self,a0)
        print(a0.size())

    def closeEvent(self, a0: QCloseEvent) -> None:
        pickle.dump(self.config,open('config.pkl','wb'))
        print('Closed')

    def enableMotors(self,value):
        if self.isRoboKittyConnected:
            if value:
                self.areMotorsEnabled = True
                AX12A.setEnableTorqueGroup(self.ax12aInstances, 1)
            else:
                self.areMotorsEnabled = False
                AX12A.setEnableTorqueGroup(self.ax12aInstances, 0)

    def tabChanged(self,index):
        if index == 0:
            self.setFixedSize(890,300)
        elif index == 1:
            self.setFixedSize(890,400)
        elif index == 2:
            self.setFixedSize(802,324)
        elif index == 3:

            self.setFixedSize(1558,619)
            self.motionRecorderTab.motors = [
                ["Front Left Shoulder", self.FrontLeftShoulder],
                ["Front Left Femur", self.FrontLeftFemer],
                ["Front Left Leg", self.FrontLeftLeg],

                ["Front Right Shoulder", self.FrontRightShoulder],
                ["Front Right Femur", self.FrontRightFemer],
                ["Front Right Leg", self.FrontRightLeg],

                ["Rear Left Shoulder", self.RearLeftShoulder],
                ["Rear Left Femur", self.RearLeftFemer],
                ["Rear Left Leg", self.RearLeftLeg],

                ["Rear Right Shoulder", self.RearRightShoulder],
                ["Rear Right Femur", self.RearRightFemer],
                ["Rear Right Leg", self.RearRightLeg],
            ]
            self.motionRecorderTab.motionDataModel.setHeaderLabels([x[0] for x in self.motionRecorderTab.motors] + ["Delay (milliseconds)","Torque"])
            self.motionRecorderTab.initValues()


    def init(self):
        self.currentChanged.connect(self.tabChanged)
        self.calibrateServoTab = CalibrateServoTab(self)
        self.setupTab = SetupTab(self)
        self.manualControlTab = ManualControlTab(self)
        self.motionRecorderTab = MotionRecorderTab(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.show()
    app.exec_()

