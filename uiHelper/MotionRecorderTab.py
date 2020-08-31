from utils.MotionRecorderTableModel import MotionRecorderTableModel
from PyQt5.QtCore import QModelIndex,QThread,pyqtSignal
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush,QColor
from utils.MotionRecorderData import MotionRecorderData
import time
from utils.AX12 import AX12A
if __name__ =='__main__':
    from RoboKitty import MainWindow

class MotionRecorderTab:

    def __init__(self,parent):
        self.maxDelay = None
        self.parent = parent # type:MainWindow
        self.motionData = [[None for x in range(14)] for x in range (1)]
        self.motionDataModel = MotionRecorderTableModel(self.motionData)
        self.parent.motionRecordTableMR.setModel(self.motionDataModel)
        self.motors = []
        self.selectedRows = None
        self.headerSelectColor = Qt.red
        self.positionGetterThread = None # type:ServoPositionGetter
        self.playMotionThread = None # type:PlayMotionThread

        self.inManualRecordMode = False

        self.inRecordingMode = False
        self.inEditMode = False
        self.currentRowIndex = 0
        self.currentColumnIndex = None

        self.previousRowIndex = None
        self.previousColumnIndex = None
        self.currentMotion = None
        self.isPlayingMotion = False
        self.init()

    def init(self):
        self.parent.motionRecordTableMR.horizontalHeader().sectionClicked.connect(lambda x: self.columnClicked(x))
        self.parent.motionRecordTableMR.verticalHeader().sectionClicked.connect(lambda x:print(x))
        self.parent.motionRecordTableMR.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.parent.editModeButtonMR.clicked.connect(self.editButtonClicked)
        self.parent.startRecordingMotionButtonMR.clicked.connect(self.startRecordingButtonClicked)
        self.parent.nextButtonMR.clicked.connect(self.nextButtonClicked)
        self.parent.motionRecordTableMR.setItemDelegate(CellEditDeligate())
        self.maxDelay = self.parent.secondsSpinMR.maximum()
        self.parent.secondsSpinMR.valueChanged.connect(self.secondSpinChanged)
        self.parent.playMotionButtonMR.clicked.connect(lambda x:self.playRecordingButtonClicked(x))
        self.parent.enableMotorsButtonMR.clicked.connect(lambda x:self.parent.enableMotors(x))
        self.parent.manualRecordButtonMR.clicked.connect(self.manualRecordModeButtonClicked)

        self.parent.frontLeftShoulderLabelMR.linkParent(self)
        self.parent.frontLeftShoulderLabelMR.setSliderAndColumn(self.parent.frontLeftShoulderSliderMR, 0)

        self.parent.frontLeftFemurLabelMR.linkParent(self)
        self.parent.frontLeftFemurLabelMR.setSliderAndColumn(self.parent.frontLeftFemurSliderMR,1)

        self.parent.frontLeftLegLabelMR.linkParent(self)
        self.parent.frontLeftLegLabelMR.setSliderAndColumn(self.parent.frontLeftLegSliderMR, 2)

        self.parent.frontRightShoulderLabelMR.linkParent(self)
        self.parent.frontRightShoulderLabelMR.setSliderAndColumn(self.parent.frontRightShoulderSliderMR, 3)

        self.parent.frontRightFemurLabelMR.linkParent(self)
        self.parent.frontRightFemurLabelMR.setSliderAndColumn(self.parent.frontRightFemurSliderMR, 4)

        self.parent.frontRightLegLabelMR.linkParent(self)
        self.parent.frontRightLegLabelMR.setSliderAndColumn(self.parent.frontRightLegSliderMR, 5)

        self.parent.rearLeftShoulderLabelMR.linkParent(self)
        self.parent.rearLeftShoulderLabelMR.setSliderAndColumn(self.parent.rearLeftShoulderSliderMR, 6)

        self.parent.rearLeftFemurLabelMR.linkParent(self)
        self.parent.rearLeftFemurLabelMR.setSliderAndColumn(self.parent.rearLeftFemurSliderMR, 7)

        self.parent.rearLeftLegLabelMR.linkParent(self)
        self.parent.rearLeftLegLabelMR.setSliderAndColumn(self.parent.rearLeftLegSliderMR, 8)

        self.parent.rearRightShoulderLabelMR.linkParent(self)
        self.parent.rearRightShoulderLabelMR.setSliderAndColumn(self.parent.rearRightShoulderSliderMR, 9)

        self.parent.rearRightFemurLabelMR.linkParent(self)
        self.parent.rearRightFemurLabelMR.setSliderAndColumn(self.parent.rearRightFemurSliderMR, 10)

        self.parent.rearRightLegLabelMR.linkParent(self)
        self.parent.rearRightLegLabelMR.setSliderAndColumn(self.parent.rearRightLegSliderMR, 11)

        self.parent.frontLeftShoulderSliderMR.linkParent(self)

        self.parent.frontLeftShoulderSliderMR.valueChanged.connect(lambda x:self.motionDataModel.setCellData(self.currentRowIndex,0,x))


    def initValues(self):
        self.parent.enableMotorsButtonMR.setChecked(self.parent.areMotorsEnabled)
        if self.parent.isRoboKittyConnected:
            self.parent.rearLeftShoulderSliderMR.setMaximum(self.parent.RearLeftShoulder.getCCWLimit())
            self.parent.rearLeftShoulderSliderMR.setMinimum(self.parent.RearLeftShoulder.getCWLimit())
            self.parent.rearLeftShoulderSliderMR.setEnabled(False)

            self.parent.frontLeftShoulderSliderMR.setMaximum(self.parent.FrontLeftShoulder.getCCWLimit())
            self.parent.frontLeftShoulderSliderMR.setMinimum(self.parent.FrontLeftShoulder.getCWLimit())
            self.parent.frontLeftShoulderSliderMR.setEnabled(False)

            self.parent.rearRightShoulderSliderMR.setMaximum(self.parent.RearRightShoulder.getCCWLimit())
            self.parent.rearRightShoulderSliderMR.setMinimum(self.parent.RearRightShoulder.getCWLimit())
            self.parent.rearRightShoulderSliderMR.setEnabled(False)

            self.parent.frontRightShoulderSliderMR.setMaximum(self.parent.FrontRightShoulder.getCCWLimit())
            self.parent.frontRightShoulderSliderMR.setMinimum(self.parent.FrontRightShoulder.getCWLimit())
            self.parent.frontRightShoulderSliderMR.setEnabled(False)

            self.parent.rearLeftFemurSliderMR.setMaximum(self.parent.RearLeftFemer.getCCWLimit())
            self.parent.rearLeftFemurSliderMR.setMinimum(self.parent.RearLeftFemer.getCWLimit())
            self.parent.rearLeftFemurSliderMR.setEnabled(False)

            self.parent.frontLeftFemurSliderMR.setMaximum(self.parent.FrontLeftFemer.getCCWLimit())
            self.parent.frontLeftFemurSliderMR.setMinimum(self.parent.FrontLeftFemer.getCWLimit())
            self.parent.frontLeftFemurSliderMR.setEnabled(False)


            self.parent.rearRightFemurSliderMR.setMaximum(self.parent.RearRightFemer.getCCWLimit())
            self.parent.rearRightFemurSliderMR.setMinimum(self.parent.RearRightFemer.getCWLimit())
            self.parent.rearRightFemurSliderMR.setEnabled(False)

            self.parent.frontRightFemurSliderMR.setMaximum(self.parent.FrontRightFemer.getCCWLimit())
            self.parent.frontRightFemurSliderMR.setMinimum(self.parent.FrontRightFemer.getCWLimit())
            self.parent.frontRightFemurSliderMR.setEnabled(False)

            self.parent.rearLeftLegSliderMR.setMaximum(self.parent.RearLeftLeg.getCCWLimit())
            self.parent.rearLeftLegSliderMR.setMinimum(self.parent.RearLeftLeg.getCWLimit())
            self.parent.rearLeftLegSliderMR.setEnabled(False)

            self.parent.frontLeftLegSliderMR.setMaximum(self.parent.FrontLeftLeg.getCCWLimit())
            self.parent.frontLeftLegSliderMR.setMinimum(self.parent.FrontLeftLeg.getCWLimit())
            self.parent.frontLeftLegSliderMR.setEnabled(False)

            self.parent.rearRightLegSliderMR.setMaximum(self.parent.RearRightLeg.getCCWLimit())
            self.parent.rearRightLegSliderMR.setMinimum(self.parent.RearRightLeg.getCWLimit())
            self.parent.rearRightLegSliderMR.setEnabled(False)

            self.parent.frontRightLegSliderMR.setMaximum(self.parent.FrontRightLeg.getCCWLimit())
            self.parent.frontRightLegSliderMR.setMinimum(self.parent.FrontRightLeg.getCWLimit())
            self.parent.frontRightLegSliderMR.setEnabled(False)

    def secondSpinChanged(self,value):
        if self.currentRowIndex is not None:
            self.motionDataModel.setCellData(self.currentRowIndex,12,value*1000)

    def millisecondSliderChanged(self,value):
        self.parent.secondsSpinMR.setValue(value/1000)

    def selectionChanged(self,x,y):
        self.selectedRows = self.parent.motionRecordTableMR.selectionModel().selectedRows() # type: QModelIndex

    def columnClicked(self,index):
        if index is not None:
            self.currentColumnIndex = index
            AX12A.setTorqueLimitGroup(self.parent.ax12aInstances,1023)
            if self.parent.isRoboKittyConnected:
                if self.motionDataModel._colorHeader[index] == self.headerSelectColor:
                    self.motionDataModel.setHeaderColor(index, Qt.black)
                    _motor = self.motors[index][1]  # type: AX12A
                    _motor.setTorque(True)
                    _motor.setTorqueLimit(1023)
                    _motor.setLED(False)
                elif index is not 12:
                    for column in range(self.motionDataModel.columnCount()):
                        if column in range(12):
                            if column == index:
                                self.motors[column][1].setTorqueLimit(1)
                                self.motors[column][1].setTorque(False)
                                self.motors[column][1].setLED(True)
                                if self.positionGetterThread is not None:
                                    self.positionGetterThread.motorIndex = column
                                self.motionDataModel.setHeaderColor(index, self.headerSelectColor)
                            else:
                                self.motors[column][1].setTorqueLimit(1023)
                                self.motors[column][1].setTorque(True)
                                self.motors[column][1].setLED(False)
                                self.motionDataModel.setHeaderColor(column, Qt.black)
        else:
            if self.parent.isRoboKittyConnected:
                self.currentColumnIndex = None
                for column in range(self.motionDataModel.columnCount()):
                    if column in range(12):
                        self.motionDataModel.setHeaderColor(column, Qt.black)
                        self.motors[column][1].setTorqueLimit(1023)
                        self.motors[column][1].setTorque(True)
                        self.motors[column][1].setLED(False)

    def editButtonClicked(self,e,manual=None):
        if self.inEditMode:
            self.inEditMode = False
            self.parent.startRecordingMotionButtonMR.setEnabled(True)
        else:
            self.inEditMode = True
            self.parent.startRecordingMotionButtonMR.setEnabled(False)

        self.motionDataModel.isEditable = self.motionDataModel.isEditable ^ True

    def startRecordingButtonClicked(self,e):
        if self.parent.isRoboKittyConnected:
            if self.inRecordingMode:
                self.parent.enableMotors(False)
                self.inRecordingMode = False
                self.positionGetterThread.stop()
                self.positionGetterThread = None
                self.parent.startRecordingMotionButtonMR.setText("Start Recording Motion")
                self.columnClicked(None)
                self.inManualRecordMode = False
                self.parent.manualRecordButtonMR.setChecked(False)
            else:
                self.parent.enableMotors(True)
                self.parent.enableMotorsButtonMR.setChecked(True)
                self.setCurrentSliderValues(self.currentRowIndex)
                self.parent.startRecordingMotionButtonMR.setText("Stop Recording Motion")
                self.inRecordingMode = True
                self.positionGetterThread = ServoPositionGetter(self)
                self.positionGetterThread.start()
                self.positionGetterThread.servoPositionSignal.connect(lambda x:self.updateMotionData(x))
        else:
            self.parent.startRecordingMotionButtonMR.setChecked(False)

    def setCurrentSliderValues(self,rowIndex):
        if self.motionData[rowIndex][0] is not None:
            self.parent.frontLeftShoulderSliderMR.setValue(self.motionData[rowIndex][0]+1)
        if self.motionData[rowIndex][1] is not None:
            self.parent.frontLeftFemurSliderMR.setValue(self.motionData[rowIndex][1]+1)
        if self.motionData[rowIndex][2] is not None:
            self.parent.frontLeftLegSliderMR.setValue(self.motionData[rowIndex][2]+1)

        if self.motionData[rowIndex][3] is not None:
            self.parent.frontRightShoulderSliderMR.setValue(self.motionData[rowIndex][3]+1)
        if self.motionData[rowIndex][4] is not None:
            self.parent.frontRightFemurSliderMR.setValue(self.motionData[rowIndex][4]+1)
        if self.motionData[rowIndex][5] is not None:
            self.parent.frontRightLegSliderMR.setValue(self.motionData[rowIndex][5]+1)

        if self.motionData[rowIndex][6] is not None:
            self.parent.rearLeftShoulderSliderMR.setValue(self.motionData[rowIndex][6]+1)
        if self.motionData[rowIndex][7] is not None:
            self.parent.rearLeftFemurSliderMR.setValue(self.motionData[rowIndex][7]+1)
        if self.motionData[rowIndex][8] is not None:
            self.parent.rearLeftLegSliderMR.setValue(self.motionData[rowIndex][8]+1)

        if self.motionData[rowIndex][9] is not None:
            self.parent.rearRightShoulderSliderMR.setValue(self.motionData[rowIndex][9]+1)
        if self.motionData[rowIndex][10] is not None:
            self.parent.rearRightFemurSliderMR.setValue(self.motionData[rowIndex][10]+1)
        if self.motionData[rowIndex][11] is not None:
            self.parent.rearRightLegSliderMR.setValue(self.motionData[rowIndex][11]+1)

    def playRecordingButtonClicked(self,e):
        if self.parent.isRoboKittyConnected:
            AX12A.setSpeedGroup(self.parent.ax12aInstances,300)
            self.playMotionThread = PlayMotionThread(self,self.motors,self.motionData)
            self.playMotionThread.start()

    def updateMotionData(self,value):
        if self.currentColumnIndex is not None:
            self.motionDataModel.setCellData(self.currentRowIndex,self.currentColumnIndex,value)
            # self.setCurrentSliderValues(self.currentRowIndex)

    def nextButtonClicked(self,e):
        self.columnClicked(None)
        self.motionData.append([None for x in range(13)])
        self.motionDataModel.layoutChanged.emit()
        self.currentRowIndex += 1
        self.parent.motionRecordTableMR.selectRow(self.currentRowIndex)
        self.secondSpinChanged(.5)

    def manualRecordModeButtonClicked(self,e):
        if self.parent.isRoboKittyConnected and self.parent.areMotorsEnabled:
            if self.inManualRecordMode:
                self.inManualRecordMode = False
                self.positionGetterThread = ServoPositionGetter(self)
                self.positionGetterThread.start()
                self.positionGetterThread.servoPositionSignal.connect(lambda x: self.updateMotionData(x))
                self.parent.manualRecordButtonMR.setText("Slider Mode")
            else:
                self.inManualRecordMode = True
                self.parent.manualRecordButtonMR.setText("Servo Mode")
                if self.positionGetterThread is not None:
                    self.positionGetterThread.stop()
        else:
            self.parent.manualRecordButtonMR.setChecked(False)

    def _test(self,e):
        self.motionDataModel.setCellData(0,7,213)

class CellEditDeligate(QtWidgets.QItemDelegate):

    def __init__(self):
        super(CellEditDeligate,self).__init__()

    def createEditor(self, parent: QtWidgets.QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QtWidgets.QWidget:
        lineEdit = QtWidgets.QLineEdit(str(index.data()), parent)
        return lineEdit

class ServoPositionGetter(QThread):
    servoPositionSignal = pyqtSignal(int)

    def __init__(self,parent):
        super(ServoPositionGetter,self).__init__()
        self.isGettingPosition = True
        self.parent = parent # type:MotionRecorderTab
        self.motorIndex = 0

    def updateMotorIndex(self,index):
        self.motorIndex = index

    def stop(self):
        self.isGettingPosition = False

    def run(self) -> None:
        while self.isGettingPosition:
            _motor = self.parent.motors[self.motorIndex][1] #  type:AX12A
            self.servoPositionSignal.emit(_motor.getPosition())
            time.sleep(1)

class PlayMotionThread(QThread):

    def __init__(self,parent,motors,data):
        super(PlayMotionThread,self).__init__()
        self.data = data
        self.parent = parent
        self.motors = motors

    def run(self) -> None:
        for data in self.data:
            print(data)
            _motionData = []
            for index, pos in enumerate(data[:11]):
                if pos is not None:
                    _motionData.append([self.motors[index][1], pos])
            AX12A.setPositionGroup(_motionData)
            _isMoving = True
            while _isMoving:
                for data in _motionData:
                    if data[0].isMoving():
                        _isMoving = True
                    else:
                        _isMoving = False