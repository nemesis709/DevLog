# -*- coding:utf-8 -*-

import sys
import pandas as pd
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QAction, QApplication, QGroupBox, QMainWindow, QTextEdit
from modules.Popup import *
from modules.FindFunction import GoTo
from modules.Items import QCentralLabel, QTable
from modules.Collections import Collect
from modules.InitFunction import First,Page
from modules.ViewFunction import View

#################### MAIN ############################
class MyApp(QMainWindow):

    ######## font ######
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./etc/D2Coding.ttf')
    app.setFont(QFont('D2Coding',15))

    def __init__(self):
        super().__init__()
        self.initUI()
        self.memlength=8
        self.index=0
        self.length=50
        self.initmem=0

    #### main layout ####
    def createMainView(self):

        #############layouts#############
        self.OVERALL_layout = QGridLayout()

        self.CONTENT_layout = QGridLayout()
        self.CONTENT = QGroupBox()
        self.CONTENT.setLayout(self.CONTENT_layout)

        ####### text for box #######
        self.LOC_text = QPushButton('Memory')
        self.HEX_text = QCentralLabel('Hex Code')
        self.BIN_text = QCentralLabel('Binary')
        self.DEC_text = QCentralLabel('Decimal')
        self.STR_text = QCentralLabel('String')
        self.COL_text = QCentralLabel('Collection')

        ####### find & goto & remove
        self.LOC_go = QPushButton('Find in Mem')
        self.HEX_find = QPushButton('Find in Hex Code')
        self.STR_find = QPushButton('Find in String')
        self.COL_remove = QPushButton('remove')
        self.COL_open = QPushButton('open')
        self.COL_save = QPushButton('save')
        self.col_layout = QGridLayout()

        self.COLTOOL = QGroupBox()
        self.COLTOOL.setLayout(self.col_layout)

        ####### box to input #######
        self.LOC = QTable(100)
        self.EDT = QTextEdit()
        self.EDT.setFixedWidth(440)
        self.HEX = QTable(440)
        self.STR = QTable(300)
        self.BIN = QTable()
        self.DEC = QTable()
        self.COL = QTable()
        self.COL.setShowGrid(True)

        ######### box layout ########
        self.CONTENT_layout.addWidget(self.LOC_text,0,0)
        self.CONTENT_layout.addWidget(self.HEX_text,0,1)
        self.CONTENT_layout.addWidget(self.BIN_text,0,3)
        self.CONTENT_layout.addWidget(self.DEC_text,0,4)
        self.CONTENT_layout.addWidget(self.COL_text,0,5)
        self.CONTENT_layout.addWidget(self.STR_text,0,2)
        
        self.CONTENT_layout.addWidget(self.LOC,1,0)
        self.CONTENT_layout.addWidget(self.HEX,1,1)
        self.CONTENT_layout.addWidget(self.EDT,1,1)
        self.CONTENT_layout.addWidget(self.BIN,1,3)
        self.CONTENT_layout.addWidget(self.DEC,1,4)
        self.CONTENT_layout.addWidget(self.COL,1,5)
        self.CONTENT_layout.addWidget(self.STR,1,2)

        self.CONTENT_layout.addWidget(self.LOC_go,2,0)
        self.CONTENT_layout.addWidget(self.HEX_find,2,1)
        self.CONTENT_layout.addWidget(self.STR_find,2,2)
        self.col_layout.addWidget(self.COL_remove,0,0)
        self.col_layout.addWidget(self.COL_open,0,1) 
        self.col_layout.addWidget(self.COL_save,0,2)
        self.CONTENT_layout.addWidget(self.COLTOOL,2,5)
        
        self.LOC_text.clicked.connect(lambda:First.setMemory(self))
        self.HEX.c.clickApp.connect(lambda:Collect.fromHEX(self))
        self.STR.c.clickApp.connect(lambda:Collect.fromSTR(self))
        self.COL.clicked.connect(lambda:Collect.Select(self))

        self.LOC_go.clicked.connect(lambda:GoTo.MEMORY(self))
        self.HEX_find.clicked.connect(lambda:GoTo.HEXA(self))
        self.STR_find.clicked.connect(lambda:GoTo.STRING(self))
        self.COL_remove.clicked.connect(lambda:Collect.Delete(self))
        self.COL_open.clicked.connect(lambda:Collect.Open(self))
        self.COL_save.clicked.connect(lambda:Collect.Save(self))
        
        #### init ####
        self.BIN.setHidden(True)
        self.BIN_text.setHidden(True)
        self.DEC.setHidden(True)
        self.DEC_text.setHidden(True)
        self.LOC.setHidden(False)
        self.LOC_text.setHidden(False)
        self.islittle=False
        self.STRmodel=pd.DataFrame([])
        self.HEXmodel=pd.DataFrame([])
        self.BINmodel=pd.DataFrame([])
        self.DECmodel=pd.DataFrame([])
        self.LOCmodel=pd.DataFrame([])
        self.COLmodel=pd.DataFrame([],columns=['LOC','S','E','HEX','STR','list'])
        

        ##### overall layout#####
        self.OVERALL_layout.addWidget(self.CONTENT,0,0)

        First.syncScrolls(self,self.LOC,self.HEX)
        First.syncScrolls(self,self.HEX,self.STR)
        First.syncScrolls(self,self.HEX,self.DEC)
        First.syncScrolls(self,self.HEX,self.BIN)

        return self.OVERALL_layout

    ######### initial UI + menubar #########
    def initUI(self):

        #main
        centralWidget = QWidget()
        centralWidget.setLayout(self.createMainView())
        self.setCentralWidget(centralWidget)

        exitButton = QAction('Exit', self)
        exitButton.setIcon(QIcon("./icons/exit.png"))
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit Application')
        exitButton.triggered.connect(QApplication.instance().quit)

        openButton = QAction('Open', self)
        openButton.setIcon(QIcon("./icons/open.png"))
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Open File')
        openButton.triggered.connect(lambda:View.CleanCol(self))
        openButton.triggered.connect(lambda:First.openFile(self))

        settingsButton = QAction('Settings',self)
        settingsButton.setIcon(QIcon("./icons/setting.png"))
        settingsButton.setShortcut('F12')
        settingsButton.setStatusTip('Open Settings')
        settingsButton.triggered.connect(lambda:First.ConfigurationClicked(self))

        findButton = QAction('Find_All',self)
        findButton.setIcon(QIcon("./icons/findall.png"))
        findButton.setShortcut('F1')
        findButton.setStatusTip('Find All in Overall Code')
        findButton.triggered.connect(lambda:Page.Select(self))

        Editing = QAction('Edit/Convert',self)
        Editing.setIcon(QIcon("./icons/edit.png"))
        Editing.setShortcut('Ctrl+E')
        Editing.setStatusTip('Edit / Convert')
        Editing.triggered.connect(lambda:First.EoC(self))

        Clearing = QAction('Clear',self)
        Clearing.setIcon(QIcon("./icons/clear.png"))
        Clearing.setShortcut('Ctrl+D')
        Clearing.setStatusTip('clear All')
        Clearing.triggered.connect(lambda:View.CleanCol(self))
        Clearing.triggered.connect(lambda:View.CleanAll(self))

        Collecting = QAction('Collect',self)
        Collecting.setIcon(QIcon("./icons/Collect.png"))
        Collecting.setShortcut('Ctrl+W')
        Collecting.setStatusTip('Collect Patterns')
        Collecting.triggered.connect(lambda:Collect.Update(self,self.COL.selectstr))

        PREV= QAction('Collect',self)
        PREV.setIcon(QIcon("./icons/left.png"))
        PREV.setShortcut('F5')
        PREV.setStatusTip('Previous')
        PREV.triggered.connect(lambda:Page.Prev(self))

        NEXT= QAction('Collect',self)
        NEXT.setIcon(QIcon("./icons/right.png"))
        NEXT.setShortcut('F6')
        NEXT.setStatusTip('Previous')
        NEXT.triggered.connect(lambda:Page.Next(self))

        #menu
        toolbar = self.addToolBar('Tools')
        menubar = self.menuBar()
        self.statusBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        fileMenu.addAction(settingsButton)
        fileMenu.addAction(openButton)        
        fileMenu.addAction(findButton)
        fileMenu.addAction(exitButton)

        editMenu.addAction(Editing)
        editMenu.addAction(Clearing)
        editMenu.addAction(Collecting)

        toolbar.addAction(exitButton)
        toolbar.addAction(settingsButton)
        toolbar.addAction(openButton)
        toolbar.addAction(findButton)
        toolbar.addAction(PREV)
        toolbar.addAction(NEXT)
        toolbar.addAction(Editing)
        toolbar.addAction(Clearing)
        toolbar.addAction(Collecting)

        ######### MAIN TITLE ##############
        self.setWindowTitle('Hex Converter')
        self.setGeometry(300, 300, 1400, 600)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())