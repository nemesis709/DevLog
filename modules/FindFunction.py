from modules.Items import QData
from modules.InitFunction import First
from modules.Popup import FindMemory, FindText
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
import pandas as pd


class Find():
    # type location to move
    def Location(self,df):
        try:
            page=df[0][:-1]
            page=int(page,16)
            page=page-self.initmem
            goto=(int(page/self.length))*self.length
            First.openFile(self,goto,filename=self.fname)
            self.LOC.clearSelection()
            model = self.LOC.model()
            start = model.index(0, 0)
            matches = model.match(
                start, QtCore.Qt.DisplayRole,
                df[0], 1, QtCore.Qt.MatchContains)
            if matches:
                index = matches[0]
                
                self.LOC.scrollTo(index)
                # self.LOC.setModel(QData(self.LOCmodel,[df[5][0],[0]]))
                self.LOC.selectionModel().setCurrentIndex(
                        index, QtCore.QItemSelectionModel.Select)
                self.HEX.setModel(QData(self.HEXmodel,line=df[-1]))
                self.STR.setModel(QData(self.STRmodel,line=df[-1]))
                self.index=goto
        except:
            pass

    # find hex and str and show result
    def HexLine(self):
        target=[]
        try:
            text=self.findtext.text
            text=text.split()[0]
            a=int(32/self.HEX.splitter)
            text=[text[i:i+a] for i in range(0, len(text), a)]      

            model=self.HEXmodel.to_numpy().flatten().tolist()
            
            for i in range(len(model)):
                match=True
                for j in range(len(text)):
                    if model[i+j]!=text[j]:
                        match=False

                if match==True:
                    for j in range(len(text)):
                        target.append(i+j)

        except:
            pass

        find_str=[[],[]]
        for i in target:
            row=i//self.HEX.splitter
            col=i%self.HEX.splitter
            find_str[0].append(row)
            find_str[1].append(col)

        
        self.HEX.setModel(QData(self.HEXmodel,line=find_str,color=QColor(0, 255, 255, 125)))
        self.STR.setModel(QData(self.STRmodel,line=find_str,color=QColor(0, 255, 255, 125)))
        rows= set(find_str[0])
        rows=list(rows)
        self.rows=rows

    def StrLine(self):
        target=[]
        try:
            text=self.findtext.text
            text=text.split()[0]
            text=list(text)

            model=self.STRmodel.to_numpy().flatten().tolist()
            
            for i in range(len(model)):
                match=True
                for j in range(len(text)):
                    if model[i+j]!=text[j]:
                        match=False

                if match==True:
                    for j in range(len(text)):
                        target.append(i+j)

        except:
            pass

        find_str=[[],[]]
        for i in target:
            row=i//self.STR.splitter
            col=i%self.STR.splitter
            find_str[0].append(row)
            find_str[1].append(col)

        self.HEX.setModel(QData(self.HEXmodel,line=find_str,color=QColor(0, 255, 255, 125)))
        self.STR.setModel(QData(self.STRmodel,line=find_str,color=QColor(0, 255, 255, 125)))
        rows= set(find_str[0])
        rows=list(rows)
        self.rows=rows

    def prevItem(self):
        try:
            self.item=(self.item+len(self.rows)-1)%len(self.rows)
            index=self.LOC.model().index(self.rows[self.item],0)
            self.LOC.scrollTo(index)
        except:
            pass
    def nextItem(self):
        try:
            self.item=(self.item+1)%len(self.rows)
            index=self.LOC.model().index(self.rows[self.item],0)
            self.LOC.scrollTo(index)
        except:
            pass

    ######### GO TO ######
class GoTo():
    def HEXA(self):
        self.rows=[]
        self.findtext = FindText(self.HEX.textcursor)
        self.findtext.show()
        self.item=0
        self.findtext.f.clickApp.connect(lambda:Find.HexLine(self))
        self.findtext.f.prev.connect(lambda:Find.prevItem(self))
        self.findtext.f.next.connect(lambda:Find.nextItem(self))
        
    def STRING(self):
        self.findtext = FindText(self.STR.textcursor)
        self.findtext.show()
        self.rows=[]
        self.item=0
        self.findtext.f.clickApp.connect(lambda:Find.StrLine(self))
        self.findtext.f.prev.connect(lambda:Find.prevItem(self))
        self.findtext.f.next.connect(lambda:Find.nextItem(self))

    def MEMORY(self):
        go = FindMemory()
        go.exec_()
        # try:
        text=go.text
        if len(text)<self.memlength:
            text=text.zfill(self.memlength)
        elif len(text)>self.memlength:
            text=text[-self.memlength:]
        if text[-1]!='0':
            text[-1]='0'
        text = pd.Series(text)
        Find.Location(self,text)
        # except:
        #     pass