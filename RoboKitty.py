from PyQt5.QtWidgets import QTabWidget,QApplication,QSizeGrip,QWidget,QVBoxLayout,QFrame,QHBoxLayout,QPushButton
from PyQt5.QtGui import QMouseEvent,QKeyEvent,QCloseEvent,QResizeEvent
import sys,pickle
from utils.ConfigFile import Config
from motionRecordUI import Ui_MainWindow
from utils.AX12 import AX12A
from PyQt5 import QtCore

from uiHelper.CalibrateServoTab import CalibrateServoTab
from uiHelper.SetupTab import SetupTab
from uiHelper.ManualControlTab import ManualControlTab
from uiHelper.MotionRecorderTab import MotionRecorderTab
from pyqt5_material import apply_stylesheet

class MainWindow(QWidget,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.config = Config()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.tabWidget = QTabWidget()
        self._mainLayout = QVBoxLayout()
        self._topBar = QHBoxLayout()
        self.windowCloseButton = QPushButton()
        self.windowCloseButton.setText("X")
        self.windowCloseButton.setFixedWidth(25)
        self.windowCloseButton.setFixedHeight(25)
        self.windowCloseButton.clicked.connect(lambda :self.close())
        self._windowMoveLine = QFrame()
        self._windowMoveLine.setFrameShadow(QFrame.Plain)
        self._windowMoveLine.setStyleSheet("background: black;")
        self._windowMoveLine.setFrameShape(QFrame.HLine)
        self._windowMoveLine.setMinimumSize(10,10)
        self._topBar.addWidget(self._windowMoveLine)
        self._topBar.addWidget((self.windowCloseButton))
        self._mainLayout.addLayout(self._topBar)
        self._mainLayout.addWidget(self.tabWidget)
        self.setLayout(self._mainLayout)
        self._windowMoveLine.mousePressEvent = self.windowBarMove
        self._windowMoveLine.mouseMoveEvent = self.windowBarMove

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
        sizeGrip = QSizeGrip(self)
        sizeGrip.setVisible(True)
        self._mainLayout.addWidget(sizeGrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.setupUi(self.tabWidget)

        self.tabWidget.setCurrentIndex(1)
        self.init()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        pass

    def windowBarMove(self,event:QMouseEvent):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.oldPos = event.globalPos()
        elif event.type() == QtCore.QEvent.MouseMove:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    # def resizeEvent(self, a0: QResizeEvent) -> None:
    #     QTabWidget.resizeEvent(self,a0)
    #     print(a0.size())

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
            pass
            # self.setFixedSize(890,300)
        elif index == 1:
            pass
            # self.setFixedSize(890,400)
        elif index == 2:
            pass
            # self.setFixedSize(802,324)
        elif index == 3:
            # self.setFixedSize(1558,619)
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
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.calibrateServoTab = CalibrateServoTab(self)
        self.setupTab = SetupTab(self)
        self.manualControlTab = ManualControlTab(self)
        self.motionRecorderTab = MotionRecorderTab(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.move(app.primaryScreen().size().width()/2-600,app.primaryScreen().size().height()/2-400)
    apply_stylesheet(app,theme='dark_teal.xml')
    windows.show()
    app.exec_()

