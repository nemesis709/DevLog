from PyQt5.QtWidgets import QFileDialog

import pandas as pd
from modules.FindFunction import Find
from modules.Items import QData


class Collect():
    #get the row info with drag
    def Update(self,list):
        # try:
            r=list[0][0]
            c=list[1]
            colloc=self.LOCmodel.iloc[r].tolist()
            colloc=colloc[0]
            start=c[0]
            t=list[0][-1]
            t=t-r+1.3
            start=self.HEXmodel.columns[start]
            end=c[-1]
            end=self.HEXmodel.columns[end]
            colhex=self.HEXmodel.iloc[r][c[0]:c[-1]+1].tolist()
            colstr=self.STRmodel.iloc[r][c[0]:c[-1]+1].tolist()
            
            if self.islittle==True:
                colhex=''.join(colhex)
                colhex = [colhex[i:i+2] for i in range(0, len(colhex), 2)]
                colhex=colhex[::-1]
                colstr=''.join(colstr)
                colstr=colstr[::-1]
                self.COL.selectstr[0]=self.COL.selectstr[0][::-1]
                self.COL.selectstr[1]=self.COL.selectstr[1][::-1]

            else:
                pass

            colhex=''.join(colhex)
            colstr=''.join(colstr)
            coldec=int(colhex,16)

            dlist=self.COL.selectstr
            nlist=[]
            for item in dlist[0]:
                
                item=item+self.index
                nlist.append(item)

            dlist[0]=nlist

            self.COLmodel=self.COLmodel.append({'LOC':colloc,'S':start,'E':end,'HEX':colhex,'STR':colstr,'DEC':coldec,'DEF':'','list':dlist},ignore_index=True)

            self.COL.setModel(QData(self.COLmodel))
            self.COL.setColumnWidth(0,80)
            self.COL.setColumnWidth(1,24)
            self.COL.setColumnWidth(2,24)
            self.COL.setColumnWidth(3,24*int((len(c)+1)/t))
            self.COL.setColumnWidth(4,17*int((len(c)+1)/t))
            self.HEX.setModel(QData(self.HEXmodel,line=self.COL.selectstr))
            self.STR.setModel(QData(self.STRmodel,line=self.COL.selectstr))

        # except:
        #     pass

        #click to move
    def Select(self):
        selection = self.COL.selectedIndexes()
        rows = sorted(index.row() for index in selection)
        mem=self.COLmodel
        mem=mem.iloc[rows[0]]
        memlist=mem.loc['list']
        memloc=mem.loc['LOC']
        memloc=memloc[:-1]
        memloc=int(memloc,16)
        memloc=memloc-self.initmem
        memloc=int(memloc/self.length)
        memloc=memloc*self.length
            
        nlist=[]
        for item in memlist[0]:
            item=item-memloc
            nlist.append(item)

        memlist2=[[],[]]
        memlist2[0]=nlist
        memlist2[1]=memlist[1]
        mem.loc['list']=memlist2
        Find.Location(self,mem)
        mem.loc['list']=memlist

    #set cursor from HEX & STR
    def fromHEX(self):
        self.COL.selectstr=self.HEX.selectstr
    def fromSTR(self):
        self.COL.selectstr=self.STR.selectstr

    # delete select row from collection
    def Delete(self):
        selection = self.COL.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            self.COLmodel=self.COLmodel.drop(self.COLmodel.index[rows[0]])
            self.COL.setModel(QData(self.COLmodel))

    #Open / Save Configs

    def Open(self):
        try:
            self.cname = QFileDialog.getOpenFileName(self, 'Open file', './cfg/')
            self.COLmodel = pd.read_pickle(self.cname[0])
            self.COL.setModel(QData(self.COLmodel))
            self.COL.setColumnWidth(0,80)
            self.COL.setColumnWidth(1,24)
            self.COL.setColumnWidth(2,24)        

        except:
            pass

    def Save(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './')
        self.cname=FileSave[0]
        print(self.cname)
        cstring=self.cname.split('/')
        if (cstring[-2]!='cfg'):
            cstring.insert(-1,'cfg')
        self.cname='/'.join(cstring)
        if(self.cname[-4:]!='.pkl'):
            self.cname=self.cname+('.pkl')
        print(self.cname)
        self.COLmodel.to_pickle(self.cname)