import pandas as pd
from Items import QData

class View():
        #show converted HEX
    def Fixed(self):
        self.HEX.setHidden(False)
        self.EDT.setHidden(True)
        # self.EDIT.setHidden(False)
        # self.Convert.setHidden(True)

    #show editing EDT
    def Editable(self):
        self.HEX.setHidden(True)
        self.EDT.setHidden(False)
        # self.EDIT.setHidden(True)
        # self.Convert.setHidden(False)

    #remove clear clean all
    def CleanAll(self):
        
        self.STR.setModel(QData(pd.DataFrame([])))
        self.DEC.setModel(QData(pd.DataFrame([])))
        self.BIN.setModel(QData(pd.DataFrame([])))
        self.HEX.setModel(QData(pd.DataFrame([])))
        self.LOC.setModel(QData(pd.DataFrame([])))
        self.EDT.clear()

        self.STR.selectstr=[]
        self.DEC.selectstr=[]
        self.BIN.selectstr=[]
        self.HEX.selectstr=[]
        self.LOC.selectstr=[]
        self.COL.selectstr=[]
        self.fname=''

    def CleanCol(self):
        self.COL.setModel(QData(pd.DataFrame([])))
        self.COLmodel=pd.DataFrame([],columns=['LOC','S','E','HEX','STR','DEC','DEF','list'])
