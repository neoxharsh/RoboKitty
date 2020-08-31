from PyQt5.QtWidgets import QTabWidget,QApplication
from PyQt5.QtGui import QMouseEvent
import sys
from motionRecordUI import Ui_MainWindow


class MainWindow(QTabWidget,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # AX12A.init()


    #
    #     canvas = QPixmap(300, 300)
    #     canvas.fill(QColor(255, 255, 255))
    #
    # def pain(self):
    #     painter = QPainter(self.paintWidget)
    #     painter.drawLine(10, 10, 300, 200)
    #     painter.end()

    def closeEvent(self, event):
        self.FrontRightLe.setTorque(0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        print(a0.x(), a0.y())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.show()
    app.exec_()

