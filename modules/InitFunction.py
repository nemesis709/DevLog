
from PyQt5.QtWidgets import QFileDialog
from modules.Popup import Configuration, InitFind, SetMemory
from modules.Items import QData
from modules.ViewFunction import View
import pandas as pd
import re


class First():

     ######## open file ########
    def openFile(self,start=0,filename=None):
        end=start+self.length-1
        View.CleanAll(self)
        if filename:
            self.fname=filename
        else:
            self.fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        # try:
    ####################################################
    #open with hex.dmp
        if re.search('.dmp$',self.fname[0]):
            with open(self.fname[0],'rb') as myfile:
                hexdata = myfile.read().hex()
                i=0
                j=start
                loc=[]

                while i<len(hexdata):
                    if j<start:
                        pass
                    locid = hex((j*16)).replace('0x','')
                    locid=locid.zfill(self.memlength)
                    loc.append(locid)
                    self.EDT.append(hexdata[i:i+32])
                    i=i+32
                    j=j+1

                    if j>end:
                        break

    ####################################################
    #open with dmp.txt
        elif re.search('.txt$',self.fname[0]):
            with open(self.fname[0],'r') as myfile:
                loc=[]
                for e,line in enumerate(myfile):
                    if(e<start):
                        pass
                    elif(e>end):
                        break
                    else:
                        line=line.split()
                        mem=line[0]
                        txt=line[1:]
                        mem=mem[:-1]
                        mem=int(mem,16)
                        if self.initmem!=0:
                            mem=mem+self.initmem
                        mem=hex(mem)
                        mem=mem.split('x')[-1]
                        mem=mem+'0'
                        mem=mem.zfill(self.memlength)
                        txt=''.join(txt)
                        loc.append(mem)
                        self.EDT.append(txt)

            self.LOCmodel=pd.DataFrame(loc,columns=['loc'])
            self.LOC.setModel(QData(self.LOCmodel))
            self.LOC.setColumnWidth(0,80)
            View.Fixed(self)
            First.CreateModel(self)

        # except:
        #     self.EDT.setText("file open error")

    ######## Config Setting ##########
    def ConfigurationClicked(self):

        cfg = Configuration()

        ############ init #########
        bin=self.BIN.isHidden()
        dec=self.DEC.isHidden()
        split_param=self.HEX.splitter
        if dec==False:
            cfg.decmod.toggle()
        if bin==False:
            cfg.binmod.toggle()
        
        if self.islittle!=cfg.endian.isChecked():
            cfg.endian.toggle()
        cfg.cutter.setCurrentIndex(cfg.cutter.findText(str(self.HEX.splitter)))
        cfg.exec_()


        ####### enable/disable BINARY & DECIMAL & collection ######
        if cfg.isdec==cfg.decmod.isChecked():
            cfg.decmod.toggle()
            dec=not cfg.isdec

        if cfg.isbin==cfg.binmod.isChecked():
            cfg.binmod.toggle()
            bin=not cfg.isbin

        self.BIN.setHidden(bin)
        self.BIN_text.setHidden(bin)
        self.DEC.setHidden(dec)
        self.DEC_text.setHidden(dec)
        
        ######### divide hex code into ######
        try:
            self.HEX.splitter=cfg.splitter
            self.Convert.clicked.connect(lambda:First.CreateModel(self))
        except:
            pass

        if split_param!=self.HEX.splitter:
            self.COLmodel=pd.DataFrame([],columns=['LOC','S','E','HEX','STR','DEC','DEF','list'])
            self.COL.setModel(QData(self.COLmodel))
            View.Fixed(self)
            First.CreateModel(self)

        ###########toggle endian
        if cfg.endian.isChecked()!=self.islittle:
            First.Tolittle(self)
            self.islittle=not self.islittle   

        if self.length!=int(cfg.line.text()):
            self.length=int(cfg.line.text())
            First.openFile(self,filename=self.fname)
            

    #converter function
    def CreateModel(self):
        
        self.STR.reset()
        self.DEC.reset()
        self.BIN.reset()

        hextext = self.EDT.toPlainText()
        hextext=re.sub(r"[^a-fA-F0-9]","",hextext)
        hextext=re.sub(r'(.{2})', r' \1', hextext)[1:]
        i=47

        while(i<len(hextext)):
            hextext = hextext[:i] + "\n" + hextext[i+1:]
            i+=48

        text = hextext.split('\n')
        self.count=int(self.HEX.splitter)
        calc=int(16/self.count)

        if self.count==8:
            column_name=['0','1','2','3','4','5','6','7']
        elif self.count==4:
            column_name=['0','1','2','3']
        elif self.count==2:
            column_name=['0','1']
        elif self.count==16:
            column_name=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']


        l10=[]
        l2=[]
        h=[]
        s=[]

        try:
            for line in text: 

                word = line.split(' ')
                d10=[]
                d2=[]
                dh=[]
                ds=[]
                    
                for w in word:

                    decode_t=int(w,16)

                    decode_w=str(w)

                    decode_10=str(decode_t)
                    decode_10=decode_10.zfill(4)
                    
                    decode_2=str(bin(decode_t))
                    decode_2=decode_2.replace('0b','')
                    decode_2=decode_2.zfill(8)

                    decode_s=chr(decode_t)

                    dh.append(decode_w)
                    d10.append(decode_10)
                    d2.append(decode_2)
                    ds.append(decode_s)



                tmph=[]
                tmps=[]
                tmp2=[]
                tmp10=[]
                

                for i in range(0,self.count):
                    joined=dh[int(calc*i):int(calc*(i+1))]
                    joined=''.join(joined)
                    tmph.append(joined)

                    joined=ds[int(calc*i):int(calc*(i+1))]
                    joined=''.join(joined)
                    tmps.append(joined)
                    
                    joined=d10[int(calc*i):int(calc*(i+1))]
                    joined=''.join(joined)
                    tmp10.append(joined)

                    joined=d2[int(calc*i):int(calc*(i+1))]
                    joined=''.join(joined)
                    tmp2.append(joined)

                    i=i+1

                d10=tmp10
                d2=tmp2
                dh=tmph
                ds=tmps


                l10.append(d10)
                l2.append(d2)
                h.append(dh)
                s.append(ds)


            self.STRmodel=pd.DataFrame(s,columns=column_name)
            self.HEXmodel=pd.DataFrame(h,columns=column_name)
            self.BINmodel=pd.DataFrame(l2,columns=column_name)
            self.DECmodel=pd.DataFrame(l10,columns=column_name)

            self.STR.setModel(QData(self.STRmodel))
            self.HEX.setModel(QData(self.HEXmodel))
            self.BIN.setModel(QData(self.BINmodel))
            self.DEC.setModel(QData(self.DECmodel))

            for i in range(0,self.count):
                self.HEX.setColumnWidth(i,24*calc+2)
                self.STR.setColumnWidth(i,15*calc+2)
                self.BIN.setColumnWidth(i,80*calc)
                self.DEC.setColumnWidth(i,40*calc)

        except:
            self.STR.setModel(QData(pd.DataFrame(["ERROR"],columns=["error!"])))

    ######## convert to little/big endian ########
    def Tolittle(self):
        hexlist = self.COLmodel['HEX'].tolist()
        strlist = self.COLmodel['STR'].tolist()
        little_hex=[]
        little_str=[]
        little_dec=[]
        
        for hex in hexlist:
            hex = [hex[i:i+2] for i in range(0, len(hex), 2)]
            hex=hex[::-1]
            hex=''.join(hex)
            dec=int(hex,16)
            little_dec.append(dec)
            little_hex.append(hex)

        for str in strlist:
            str=str[::-1]
            str=''.join(str)
            little_str.append(str)
        
        self.COLmodel['HEX']=little_hex
        self.COLmodel['STR']=little_str
        self.COLmodel['DEC']=little_dec


    ######## scroll sync ########
    def syncScrolls(self,qTextObj0, qTextObj1):

        scroll0 = qTextObj0.verticalScrollBar()
        scroll1 = qTextObj1.verticalScrollBar()

        scroll0.valueChanged.connect(    
            scroll1.setValue
        )

        scroll1.valueChanged.connect(    
            scroll0.setValue
        )


    def EoC(self):
        if self.HEX.isHidden()==True:
            First.CreateModel(self)
            View.Fixed(self)
        else:
            View.Editable(self)

    def setMemory(self):
        self.initmem = SetMemory()
        self.initmem.show()

        self.initmem.pushButton.clicked.connect(lambda:First.Add(self,self.initmem.memory.text()))

    def Add(self,text):
        text=text[:-1]
        text=int(text,16)
        self.initmem=text
        try:
            First.openFile(self,self.index,filename=self.fname)
        except:
            pass

class Page():
    def Select(self):
        self.initFinder=InitFind()
        self.initFinder.show()

        self.initFinder.pushButton.clicked.connect(lambda:Page.Find(self,self.initFinder,self.initFinder.text))
        self.initFinder.goButton.clicked.connect(lambda:Page.Move(self))

        
    def Find(self,initFinder,target):
        targetlist=[]
        bef_txt=""
        param = self.initFinder.findfor.currentIndex()
        try:
            if param==0:
                pass
            elif param==1:
                target=hex(int(target)).split('x')[-1]
            elif param==2:
                hlist=[]
                for i in list(target):
                    i=hex(ord(i)).split('x')[-1]
                    hlist.append(i)
                hlist=''.join(hlist)

                target = hlist
        except:
            pass

        # self.fname
        try:
            with open(self.fname[0],'r') as myfile:
                for line in myfile:
                    line=line.split()
                    mem=line[0]
                    txt=line[1:]
                    txt=''.join(txt)
                    
                    target_txt=[]
                    target_txt.append(bef_txt)
                    target_txt.append(txt)
                    target_txt=''.join(target_txt)

                    if target in target_txt:
                        targetlist.append(mem)

                    bef_txt=txt
                    
                nums=[]
                for t in targetlist:
                    nums.append(targetlist.index(t))

                nums=pd.DataFrame({'#':nums})
                targetlist=pd.DataFrame({"list":targetlist})
                targetlist=pd.concat([nums, targetlist], axis=1)
                initFinder.findLOC.setModel(QData(targetlist))
                initFinder.findLOC.setColumnWidth(0,20)
                initFinder.findLOC.setColumnWidth(1,80)

        except:
            pass

    def Move(self):
        try:
            mem = self.initFinder.findLOC.textcursor
            mem=mem[:-1]
            mem = int(mem,16)

            if mem<self.length:
                First.openFile(self,0,filename=self.fname)
                self.index=0
            else:
                mem=(int((mem-self.length)/self.length)+1)*self.length
                First.openFile(self,mem,filename=self.fname)
                self.index=mem

        except:
            pass

    def Prev(self):
        if self.index-self.length<self.length:
            self.index=0
        else:
            self.index=self.index-self.length
        First.openFile(self,self.index,filename=self.fname)

    def Next(self):
        if QData(self.LOCmodel).rowCount()==0:
            self.STR.setModel(QData(pd.DataFrame(["EOF"],columns=["error!"])))
        else:
            self.index=self.index+self.length
            First.openFile(self,self.index,filename=self.fname)
