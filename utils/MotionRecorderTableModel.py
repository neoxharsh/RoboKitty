from PyQt5.QtGui import QColor, QStandardItemModel, QBrush
from PyQt5.QtCore import QAbstractTableModel, QModelIndex
from PyQt5.Qt import Qt
import numbers

class MotionRecorderTableModel(QAbstractTableModel):

    def __init__(self, data):
        self._data = data  # type:list
        self._labels = None
        self._colorCell = dict()
        self._colorHeader = dict
        self.isEditable = False
        super(MotionRecorderTableModel, self).__init__()

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._data[index.row()][index.column()]
        if role == Qt.BackgroundRole:
            color = self._colorCell.get((index.row(), index.column()))
            if color is not None:
                return QBrush(color)

    def flags(self, index):
        if self.isEditable:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsSelectable

    def setData(self, index: QModelIndex, value, role: int = ...) -> bool:
        if role==Qt.EditRole:
            if value == "":
                self._data[index.row()][index.column()] = None
                return True
            try:
                if int(value) >= 0:
                    self._data[index.row()][index.column()] = int(value)
                    print(type(self._data[index.row()][index.column()]))
                    return True
                else:
                    return True
            except:
                return True

    def setHeaderLabels(self, labels):
        self._labels = labels
        self._colorHeader = {x: Qt.black for x in range(len(labels))}

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data[0])

    def setCellColour(self,row,column,color):
        self._colorCell[(row, column)] = color
        self.dataChanged.emit(self.index(row,column),self.index(row,column),(Qt.BackgroundRole,))

    def setCellData(self,row,column,value):
        self._data[row][column] = value
        self.dataChanged.emit(self.index(row, column), self.index(row, column), (Qt.DisplayRole,))

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) :
        try:
            if role == Qt.DisplayRole:
                if orientation == Qt.Horizontal and self._labels is not None:
                    return str(self._labels[section])
                if orientation == Qt.Vertical:
                    return str(section)
            if role == Qt.ForegroundRole and orientation == Qt.Horizontal:
                color = self._colorHeader.get(section)
                if color is not None:
                    return QBrush(color)
        except:
            pass

    def setHeaderColor(self,index,color):
        self._colorHeader[index] = color
        self.headerDataChanged.emit(Qt.Horizontal,1,10)
