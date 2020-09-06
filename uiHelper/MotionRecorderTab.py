from utils.MotionRecorderTableModel import MotionRecorderTableModel
from PyQt5.QtCore import QModelIndex,QThread,pyqtSignal
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from uiHelper.CustomQLabel import CustomQLabel
import time,pickle,os
from utils.AX12 import AX12A
if __name__ =='__main__':
    from RoboKitty import MainWindow

class MotionRecorderTab:

    def __init__(self,parent):
        self.maxDelay = None
        self.parent = parent # type:MainWindow
        self.motionData = [[None for x in range(14)]]
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
        self.currentMotionSelectIndex = None
        self.savedMotionList = None

        self.previousRowIndex = None
        self.previousColumnIndex = None
        self.currentMotion = None
        self.isPlayingMotion = False
        self.singleColumnSelectMode = True
        self.init()

    def init(self):
        self.parent.motionRecordTableMR.horizontalHeader().sectionClicked.connect(lambda x: self.columnClicked(x))
        self.parent.motionRecordTableMR.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.parent.editModeButtonMR.clicked.connect(self.editButtonClicked)
        self.parent.startRecordingMotionButtonMR.clicked.connect(self.startRecordingButtonClicked)
        self.parent.addNewRowButtonMR.clicked.connect(self.addNewRowButtonClicked)
        self.parent.motionRecordTableMR.setItemDelegate(CellEditDelegate())
        self.maxDelay = self.parent.secondsSpinMR.maximum()
        self.parent.secondsSpinMR.valueChanged.connect(self.secondSpinChanged)
        self.parent.playMotionButtonMR.clicked.connect(lambda x:self.playRecordingButtonClicked(x))
        self.parent.enableMotorsButtonMR.clicked.connect(lambda x:self.parent.enableMotors(x))
        self.parent.manualRecordButtonMR.clicked.connect(self.manualRecordModeButtonClicked)
        self.parent.torqueSliderMR.valueChanged.connect(self.torqueSliderChanged)
        self.parent.saveMotionButtonMR.clicked.connect(self.saveMotionButtonClicked)
        self.parent.motionsListViewMR.itemSelectionChanged.connect(self.motionSelectIndexChanged)
        self.parent.loadMotionButtonMR.clicked.connect(self.loadMotionButtonClicked)
        self.parent.newMotionButtonMR.clicked.connect(self.newMotionButtonClicked)
        self.parent.appendMotionButton.clicked.connect(self.appendMotionButtonClicked)
        self.parent.singleJointSelectModeRadioButtonMR.toggled.connect(lambda :self.columnSelectMode(self.parent.singleJointSelectModeRadioButtonMR))
        self.parent.multiJointSelectModeRadioButtonMR.toggled.connect(lambda :self.columnSelectMode(self.parent.multiJointSelectModeRadioButtonMR))

        for column in range(self.motionDataModel.columnCount()):
            self.parent.motionRecordTableMR.setColumnWidth(column,200)
        self.parent.frontLeftShoulderLabelMR.setParentSliderColumn(self,self.parent.frontLeftShoulderSliderMR, 0)

        self.parent.frontLeftFemurLabelMR.setParentSliderColumn(self,self.parent.frontLeftFemurSliderMR, 1)


        self.parent.frontLeftLegLabelMR.setParentSliderColumn(self,self.parent.frontLeftLegSliderMR, 2)


        self.parent.frontRightShoulderLabelMR.setParentSliderColumn(self,self.parent.frontRightShoulderSliderMR, 3)


        self.parent.frontRightFemurLabelMR.setParentSliderColumn(self,self.parent.frontRightFemurSliderMR, 4)


        self.parent.frontRightLegLabelMR.setParentSliderColumn(self,self.parent.frontRightLegSliderMR, 5)


        self.parent.rearLeftShoulderLabelMR.setParentSliderColumn(self,self.parent.rearLeftShoulderSliderMR, 6)


        self.parent.rearLeftFemurLabelMR.setParentSliderColumn(self,self.parent.rearLeftFemurSliderMR, 7)


        self.parent.rearLeftLegLabelMR.setParentSliderColumn(self,self.parent.rearLeftLegSliderMR, 8)


        self.parent.rearRightShoulderLabelMR.setParentSliderColumn(self,self.parent.rearRightShoulderSliderMR, 9)


        self.parent.rearRightFemurLabelMR.setParentSliderColumn(self,self.parent.rearRightFemurSliderMR, 10)


        self.parent.rearRightLegLabelMR.setParentSliderColumn(self,self.parent.rearRightLegSliderMR, 11)

        self.parent.frontLeftShoulderSliderMR.setParentAndColumn(self,0)
        self.parent.frontLeftFemurSliderMR.setParentAndColumn(self,1)
        self.parent.frontLeftLegSliderMR.setParentAndColumn(self,2)

        self.parent.frontRightShoulderSliderMR.setParentAndColumn(self, 3)
        self.parent.frontRightFemurSliderMR.setParentAndColumn(self, 4)
        self.parent.frontRightLegSliderMR.setParentAndColumn(self, 5)

        self.parent.rearLeftShoulderSliderMR.setParentAndColumn(self,6)
        self.parent.rearLeftFemurSliderMR.setParentAndColumn(self,7)
        self.parent.rearLeftLegSliderMR.setParentAndColumn(self,8)

        self.parent.rearRightShoulderSliderMR.setParentAndColumn(self, 9)
        self.parent.rearRightFemurSliderMR.setParentAndColumn(self, 10)
        self.parent.rearRightLegSliderMR.setParentAndColumn(self, 11)

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

            self.parent.frontLeftShoulderLabelMR.setMotor(self.motors[0][1])
            self.parent.frontLeftFemurLabelMR.setMotor(self.motors[1][1])
            self.parent.frontLeftLegLabelMR.setMotor(self.motors[2][1])

            self.parent.frontRightShoulderLabelMR.setMotor(self.motors[3][1])
            self.parent.frontRightFemurLabelMR.setMotor(self.motors[4][1])
            self.parent.frontRightLegLabelMR.setMotor(self.motors[5][1])

            self.parent.rearLeftShoulderLabelMR.setMotor(self.motors[6][1])
            self.parent.rearLeftFemurLabelMR.setMotor(self.motors[7][1])
            self.parent.rearLeftLegLabelMR.setMotor(self.motors[8][1])

            self.parent.rearRightShoulderLabelMR.setMotor(self.motors[9][1])
            self.parent.rearRightFemurLabelMR.setMotor(self.motors[10][1])
            self.parent.rearRightLegLabelMR.setMotor(self.motors[11][1])

            self.parent.frontLeftShoulderSliderMR.setMotor(self.motors[0][1])
            self.parent.frontLeftFemurSliderMR.setMotor(self.motors[1][1])
            self.parent.frontLeftLegSliderMR.setMotor(self.motors[2][1])

            self.parent.frontRightShoulderSliderMR.setMotor(self.motors[3][1])
            self.parent.frontRightFemurSliderMR.setMotor(self.motors[4][1])
            self.parent.frontRightLegSliderMR.setMotor(self.motors[5][1])

            self.parent.rearLeftShoulderSliderMR.setMotor(self.motors[6][1])
            self.parent.rearLeftFemurSliderMR.setMotor(self.motors[7][1])
            self.parent.rearLeftLegSliderMR.setMotor(self.motors[8][1])

            self.parent.rearRightShoulderSliderMR.setMotor(self.motors[9][1])
            self.parent.rearRightFemurSliderMR.setMotor(self.motors[10][1])
            self.parent.rearRightLegSliderMR.setMotor(self.motors[11][1])
            self.savedMotionList = [x for x in os.listdir('motions')]
            self.parent.motionsListViewMR.clear()
            self.parent.motionsListViewMR.addItems(self.savedMotionList)

    def secondSpinChanged(self,value):
        if self.currentRowIndex is not None:
            self.motionDataModel.setCellData(self.currentRowIndex,12,value*1000)

    def torqueSliderChanged(self,value):
        if self.currentRowIndex is not None:
            self.motionDataModel.setCellData(self.currentRowIndex,13,value)

    def selectionChanged(self,x,y):
        if len(self.parent.motionRecordTableMR.selectionModel().selectedRows())>0:
            self.currentRowIndex = self.parent.motionRecordTableMR.selectionModel().selectedRows()[0].row() # type: QModelIndex
            CustomQLabel.disableAll()
        else:
            pass

    def columnSelectMode(self,_sender):
        if _sender == self.parent.singleJointSelectModeRadioButtonMR and self.parent.singleJointSelectModeRadioButtonMR.isChecked():
            self.singleColumnSelectMode = True
        if _sender == self.parent.multiJointSelectModeRadioButtonMR and self.parent.multiJointSelectModeRadioButtonMR.isChecked():
            self.singleColumnSelectMode = False

    def columnClicked(self,index):
        if index is not None:
            AX12A.setTorqueLimitGroup(self.parent.ax12aInstances,1023)
            if self.parent.isRoboKittyConnected:
                if self.motionDataModel._colorHeader[index] == self.headerSelectColor:
                    self.motionDataModel.setHeaderColor(index, Qt.black)
                    _motor = self.motors[index][1]  # type: AX12A
                    _motor.setTorque(True)
                    _motor.setTorqueLimit(1023)
                    _motor.setLED(False)
                    self.currentColumnIndex =None
                elif index is not 12:
                    for column in range(self.motionDataModel.columnCount()):
                        if column in range(12):
                            if self.singleColumnSelectMode:
                                if column == index:
                                    self.motors[column][1].setTorqueLimit(1)
                                    self.motors[column][1].setTorque(False)
                                    self.motors[column][1].setLED(True)
                                    if self.positionGetterThread is not None:
                                        self.positionGetterThread.motorIndex = column
                                    self.motionDataModel.setHeaderColor(index, self.headerSelectColor)
                                    self.currentColumnIndex = index
                                else:
                                    self.motors[column][1].setTorqueLimit(1023)
                                    self.motors[column][1].setTorque(True)
                                    self.motors[column][1].setLED(False)
                                    self.motionDataModel.setHeaderColor(column, Qt.black)
                            else:
                                if column == index:
                                    self.motors[column][1].setTorqueLimit(1)
                                    self.motors[column][1].setTorque(False)
                                    self.motors[column][1].setLED(True)
                                    if self.positionGetterThread is not None:
                                        self.positionGetterThread.motorIndex = column
                                    self.motionDataModel.setHeaderColor(index, self.headerSelectColor)
                                    self.currentColumnIndex = index
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
            self.parent.playMotionButtonMR.setEnabled(True)
            self.parent.torqueSliderMR.setEnabled(False)
            self.parent.secondsSpinMR.setEnabled(False)

            self.parent.saveMotionButtonMR.setEnabled(True)
            self.parent.loadMotionButtonMR.setEnabled(True)
            self.parent.appendMotionButton.setEnabled(True)
            self.parent.newMotionButtonMR.setEnabled(True)
            self.parent.startRecordingMotionButtonMR.setEnabled(True)
        else:
            self.inEditMode = True
            self.parent.torqueSliderMR.setEnabled(True)
            self.parent.secondsSpinMR.setEnabled(True)
            self.parent.startRecordingMotionButtonMR.setEnabled(False)
            self.parent.playMotionButtonMR.setEnabled(False)

            self.parent.saveMotionButtonMR.setEnabled(False)
            self.parent.loadMotionButtonMR.setEnabled(False)
            self.parent.appendMotionButton.setEnabled(False)
            self.parent.newMotionButtonMR.setEnabled(False)
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
                self.parent.playMotionButtonMR.setEnabled(True)
                CustomQLabel.disableAll()
                self.parent.motionRecordTableMR.setEnabled(True)
                self.parent.torqueSliderMR.setEnabled(False)
                self.parent.secondsSpinMR.setEnabled(False)
                self.parent.saveMotionButtonMR.setEnabled(True)
                self.parent.loadMotionButtonMR.setEnabled(True)
                self.parent.appendMotionButton.setEnabled(True)
                self.parent.newMotionButtonMR.setEnabled(True)
                self.parent.editModeButtonMR.setEnabled(True)
            else:
                self.parent.torqueSliderMR.setEnabled(True)
                self.parent.secondsSpinMR.setEnabled(True)
                self.parent.playMotionButtonMR.setEnabled(False)

                self.parent.saveMotionButtonMR.setEnabled(False)
                self.parent.loadMotionButtonMR.setEnabled(False)
                self.parent.appendMotionButton.setEnabled(False)
                self.parent.newMotionButtonMR.setEnabled(False)
                self.parent.editModeButtonMR.setEnabled(False)

                self.parent.enableMotors(True)
                self.parent.enableMotorsButtonMR.setChecked(True)
                self.parent.startRecordingMotionButtonMR.setText("Stop Recording Motion")
                self.inRecordingMode = True
                self.currentRowIndex = self.motionDataModel.rowCount()-1
                self.parent.motionRecordTableMR.selectRow(self.currentRowIndex)
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
        if self.parent.isRoboKittyConnected and not self.isPlayingMotion:
            AX12A.setSpeedGroup(self.parent.ax12aInstances,1023)
            self.isPlayingMotion = True
            self.parent.enableMotorsButtonMR.setChecked(True)
            self.parent.enableMotorsButtonMR.setEnabled(False)
            self.playMotionThread = PlayMotionThread(self,self.motors,self.motionData)
            self.playMotionThread.finishSignal.connect(lambda :self.parent.playMotionButtonMR.setChecked(False))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.playMotionButtonMR.setText("Play Motion"))
            self.playMotionThread.stepSignal.connect(lambda x:self.parent.motionRecordTableMR.selectRow(x))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.enableMotorsButtonMR.setEnabled(True))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.saveMotionButtonMR.setEnabled(True))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.loadMotionButtonMR.setEnabled(True))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.appendMotionButton.setEnabled(True))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.newMotionButtonMR.setEnabled(True))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.startRecordingMotionButtonMR.setEnabled(True))
            self.playMotionThread.finishSignal.connect(lambda :self.parent.editModeButtonMR.setEnabled(True))
            self.playMotionThread.start()
            self.parent.playMotionButtonMR.setText("Stop Motion")
            self.parent.saveMotionButtonMR.setEnabled(False)
            self.parent.loadMotionButtonMR.setEnabled(False)
            self.parent.appendMotionButton.setEnabled(False)
            self.parent.newMotionButtonMR.setEnabled(False)
            self.parent.startRecordingMotionButtonMR.setEnabled(False)
            self.parent.editModeButtonMR.setEnabled(False)
        else:
            self.parent.playMotionButtonMR.setText("Play Motion")
            if self.playMotionThread is not None and self.playMotionThread.running:
                self.playMotionThread.stop()

    def updateMotionData(self,value):
        if self.currentColumnIndex is not None:
            self.motionDataModel.setCellData(self.currentRowIndex,self.currentColumnIndex,value)

    def addNewRowButtonClicked(self,e):
        if self.inRecordingMode:
            self.columnClicked(None)
            self.motionData.append([None for x in range(14)])
            self.motionDataModel.layoutChanged.emit()
            self.currentRowIndex = self.motionDataModel.rowCount()-1
            self.parent.motionRecordTableMR.selectRow(self.currentRowIndex)
            self.secondSpinChanged(.5)
            CustomQLabel.disableAll()

    def manualRecordModeButtonClicked(self,e):
        if self.parent.isRoboKittyConnected and self.parent.areMotorsEnabled and self.inRecordingMode:
            CustomQLabel.disableAll()
            if self.inManualRecordMode:
                self.inManualRecordMode = False
                self.positionGetterThread = ServoPositionGetter(self)
                self.positionGetterThread.start()
                self.currentColumnIndex = None
                self.positionGetterThread.servoPositionSignal.connect(lambda x: self.updateMotionData(x))
                self.parent.manualRecordButtonMR.setText("Slider Mode")
                self.parent.manualSlidersLayoutMR.setEnabled(False)
                self.parent.motionRecordTableMR.setEnabled(True)
            else:
                self.inManualRecordMode = True
                self.parent.manualRecordButtonMR.setText("Servo Mode")
                self.parent.manualSlidersLayoutMR.setEnabled(True)
                for column in range(12):
                    self.motionDataModel.setHeaderColor(column,Qt.black)
                    self.motors[column][1].setTorqueLimit(1023)
                    self.motors[column][1].setTorque(True)
                    self.motors[column][1].setLED(False)
                self.parent.motionRecordTableMR.setEnabled(False)
                if self.positionGetterThread is not None:
                    self.positionGetterThread.stop()
        else:
            self.parent.manualRecordButtonMR.setChecked(False)

    def saveMotionButtonClicked(self,e):
        if not self.parent.motionNameLineEditMR.text().isspace() and self.parent.motionNameLineEditMR.text() != "":
            pickle.dump(self.motionData,open("motions/"+self.parent.motionNameLineEditMR.text(),'wb'))
            if self.parent.motionNameLineEditMR.text() not in self.savedMotionList:
                self.savedMotionList.append(self.parent.motionNameLineEditMR.text())
                self.parent.motionsListViewMR.addItem(self.parent.motionNameLineEditMR.text())

    def motionSelectIndexChanged(self):
        self.currentMotionSelectIndex = self.parent.motionsListViewMR.currentRow()

    def appendMotionButtonClicked(self,e):
        if self.currentMotionSelectIndex is not None:
            tempMotionData = pickle.load(open("motions/" + self.savedMotionList[self.currentMotionSelectIndex], 'rb'))
            self.motionData = self.motionData + tempMotionData
            self.motionDataModel.updateData(self.motionData)

    def loadMotionButtonClicked(self,e):
        if self.currentMotionSelectIndex is not None:
            self.motionData = pickle.load(open("motions/"+self.savedMotionList[self.currentMotionSelectIndex],'rb'))
            self.motionDataModel.updateData(self.motionData)

    def newMotionButtonClicked(self,e):
        if not self.inRecordingMode and self.parent.isRoboKittyConnected:
            self.motionData = [[None for x in range(14)]]
            self.motionDataModel.updateData(self.motionData)


class CellEditDelegate(QtWidgets.QItemDelegate):

    def __init__(self):
        super(CellEditDelegate, self).__init__()

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
            if self.parent.singleColumnSelectMode:
                _motor = self.parent.motors[self.motorIndex][1]  # type:AX12A
                self.servoPositionSignal.emit(_motor.getPosition())
            else:
                _motor = self.parent.motors[self.motorIndex][1]  # type:AX12A
                self.servoPositionSignal.emit(_motor.getPosition())
            time.sleep(1)

class PlayMotionThread(QThread):

    stepSignal = pyqtSignal(int)
    finishSignal = pyqtSignal()

    def __init__(self,parent,motors,data):
        super(PlayMotionThread,self).__init__()
        self.data = data
        self.parent = parent
        self.motors = motors
        self.running = True

    def stop(self):
        self.running = False

    def run(self) -> None:
        for index,data in enumerate(self.data):
            if not self.running:
                break
            self.stepSignal.emit(index)
            _motionData = []
            for index, pos in enumerate(data[:12]):
                if pos is not None:
                    _motionData.append([self.motors[index][1], pos])
            if data[13] is not None or data[13] is 0:
                AX12A.setTorqueLimitGroup([motor[0] for motor in _motionData],data[13])
            if len(_motionData)>0:
                AX12A.setPositionGroup(_motionData)
                _isMoving = True
                while _isMoving:
                    for _data in _motionData:
                        if _data[0].isMoving():
                            _isMoving = True
                        else:
                            _isMoving = False
                AX12A.setTorqueLimitGroup([motor[0] for motor in _motionData],1023)
                try:
                    time.sleep(data[12]/1000)
                except Exception as e:
                    pass
        self.finishSignal.emit()
        self.parent.isPlayingMotion = False
