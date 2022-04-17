from Items import QTable
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QLabel, QTableView, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QPushButton
from PyQt5 import QtCore

    

    ############ ClickSignal ############
class ClickSignal(QtCore.QObject):
    clickApp = QtCore.pyqtSignal()
    prev = QtCore.pyqtSignal()
    next = QtCore.pyqtSignal()

############ FindMemory ############
class FindMemory(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Find Memory Location")

        layout = QGridLayout()

        self.memory = QLineEdit()
        self.pushButton = QPushButton("OK")

        layout.addWidget(self.memory, 0, 0)
        layout.addWidget(self.pushButton, 0, 1)

        self.setLayout(layout)

        self.pushButton.clicked.connect(self.pushButtonClicked)

    def pushButtonClicked(self):
        self.text=self.memory.text()
        self.close()

############ Find HEX pattern ############
class FindText(QWidget):
    def __init__(self,text):
        super().__init__()
        self.setupUI(text)
        self.f=ClickSignal()

    def keyPressEvent(self, e):
        if e.key()  == QtCore.Qt.Key_Return:
            self.pushButtonClicked()

    def setupUI(self,text):
        self.setGeometry(1100, 200, 400, 100)
        self.setWindowTitle("Find")

        layout = QGridLayout()
        self.memory = QLineEdit(text)
        self.pushButton = QPushButton("OK")
        self.prevButton = QPushButton("prev")
        self.nextButton = QPushButton("next")

        layout.addWidget(self.memory, 0, 0)
        layout.addWidget(self.pushButton, 0, 5)
        layout.addWidget(self.prevButton, 1, 4)
        layout.addWidget(self.nextButton, 1, 5)

        self.setLayout(layout)

        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.prevButton.clicked.connect(self.prevClicked)
        self.nextButton.clicked.connect(self.nextClicked)
        self.pushButton.keyPressEvent=self.keyPressEvent

    def pushButtonClicked(self):
        self.text=self.memory.text()
        self.f.clickApp.emit()

    def prevClicked(self):
        self.f.prev.emit()

    def nextClicked(self):
        self.f.next.emit()

############# CONFIG ############
class Configuration(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.isdec=False
        self.isbin=False
        self.iscol=True
        self.quit=False

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Settings")

        layout = QGridLayout()

        self.pushButton = QPushButton("Confirm")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.endian = QCheckBox('Little Endian')
        self.decmod=QCheckBox("DECIMAL")
        self.binmod=QCheckBox("BINARY")
        self.cutinto=QLabel("divide into:")
        self.cutter=QComboBox()
        self.cutter.addItems(["16","8","4","2"])
        self.liner=QLabel("show lines:")
        self.line=QLineEdit("50")


        layout.addWidget(self.pushButton, 0, 0)
        layout.addWidget(self.endian,1,0)
        layout.addWidget(self.decmod, 2, 0)
        layout.addWidget(self.binmod, 3, 0)
        layout.addWidget(self.cutinto,5,0)
        layout.addWidget(self.cutter,5,1)
        layout.addWidget(self.liner,6,0)
        layout.addWidget(self.line,6,1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.isdec=self.decmod.isChecked()
        self.isbin=self.binmod.isChecked()
        self.splitter=int(self.cutter.currentText())
        self.little=self.endian.isChecked()
        self.quit=True
        self.close()

############ Find HEX pattern ############
class InitFind(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.g=ClickSignal()

    def setupUI(self):
        self.setGeometry(300, 200, 200, 300)
        self.setWindowTitle("Search Text")
        

        layout0 = QGridLayout()
        layout1 = QGridLayout()
        layout2 = QGridLayout()
        Mlayout = QVBoxLayout()
        self.findfor = QComboBox()
        self.findfor.addItems(["HEX","DEC","STR"])
        self.memory = QLineEdit()
        self.pushButton = QPushButton("Find")
        self.goButton = QPushButton("Go")
        self.findLOC = QTable()
        self.findLOC.setColumnWidth(0,60)

        layout0.addWidget(self.findfor,0,0)
        layout1.addWidget(self.memory, 1, 0)
        layout1.addWidget(self.pushButton, 1, 1)
        layout2.addWidget(self.findLOC, 1, 0)
        layout2.addWidget(self.goButton, 2,0)
        Mlayout.addLayout(layout0)
        Mlayout.addLayout(layout1)
        Mlayout.addLayout(layout2)

        self.setLayout(Mlayout)
        self.pushButton.clicked.connect(self.pushButtonClicked)

    def pushButtonClicked(self):
        self.text=self.memory.text()

#######set initial memory
class SetMemory(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Set Initial Memory")

        layout = QGridLayout()

        self.memory = QLineEdit()
        self.pushButton = QPushButton("OK")

        layout.addWidget(self.memory, 0, 0)
        layout.addWidget(self.pushButton, 0, 1)

        self.setLayout(layout)

        self.pushButton.clicked.connect(self.pushButtonClicked)

    def pushButtonClicked(self):
        self.text=self.memory.text()
        self.close()