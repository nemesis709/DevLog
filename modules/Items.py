from PyQt5 import QtCore
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QLabel, QTableView
import csv
import io


############ ClickSignal ############
class ClickSignal(QtCore.QObject):
    clickApp = QtCore.pyqtSignal()

############ data table ############
class QData(QtCore.QAbstractTableModel):

    def __init__(self, data, line=None, color=None, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.line = line
        self.color = color
 
    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def flags(self, index):
            if not index.isValid():
                return QtCore.Qt.ItemIsEnabled

            return super().flags(index) | QtCore.Qt.ItemIsEditable  # add editable flag.

    def setData(self, index, value, role):
            if role == QtCore.Qt.EditRole:
                # Set the value into the frame.
                self._data.iloc[index.row(), index.column()] = value
                return True

            return False

    def data(self, index, role, line=None, color=None):
        try:
            line=self.line
            color=self.color
            if index.isValid():
                if role == QtCore.Qt.DisplayRole:
                    if(index.column() != 0):
                        return str('%s'%self._data.values[index.row()][index.column()])
                    else:
                        return str(self._data.values[index.row()][index.column()])

            
            if line:
                for i in range(len(line[0])):
                    if role == QtCore.Qt.BackgroundRole:
                        if(index.row() == line[0][i]):
                            if(index.column() == line[1][i]):
                                if color:
                                    paint=color
                                else:
                                    paint=QColor(255, 0, 255, 125)
                                return QBrush(paint)
        except:
            pass
        return None

    def headerData(self, section, orientation, role):
        try:
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self._data.columns[section]
            elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
                return str(self._data.index[section])
        except:
            pass          
        return None


############ Main Table ############
class QTable(QTableView):
    def __init__(self, value=0, parent=None):
        QTableView.__init__(self, parent)
        self.setFont(QFont('D2Coding',15))
        if value!=0:
            self.setFixedWidth(value)
        self.setShowGrid(False)
        self.setMouseTracking(False)
        self.verticalHeader().hide()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers |
                             QAbstractItemView.DoubleClicked)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.splitter=16
        self.textcursor=''
        self.selectstr=[]
        self.c=ClickSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.mouseReleaseEvent

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.Drag()
        self.c.clickApp.emit()
        
    #drag string-> cursor, copy
    def Drag(self):
        self.selectstr=[]
        selection = self.selectedIndexes()
        if selection:
            rows=[]
            columns=[]
            for index in selection:
                rows.append(index.row())
                columns.append(index.column())
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]

            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
                
            self.selectstr.append(rows)
            self.selectstr.append(columns)
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            cpstr=stream.getvalue()
            cpstr=cpstr.replace(',','')
            cpstr=cpstr[:-2]
            self.textcursor=cpstr
            QApplication.clipboard().setText(cpstr)

    ############ label in central ############
class QCentralLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setAlignment(QtCore.Qt.AlignCenter)