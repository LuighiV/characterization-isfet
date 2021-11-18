# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 09:44:21 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui,QtCore

class GUI(QtGui.QMainWindow):
    
    def __init__(self,parent=None):
        super(GUI,self).__init__()
        
        self.initGUI()
        self.show()
        
    def initGUI(self):
        
        self.setWindowTitle("Measurements Launcher")
        
        mwidget = QtGui.QWidget(self)
        self.setCentralWidget(mwidget)
        
        buttonsw = QtGui.QWidget(mwidget)
        self.appac = QtGui.QGroupBox(mwidget)
        self.appac.setMinimumHeight(300)
        self.appac.setMinimumWidth(200)
        
        self.appproc = QtGui.QGroupBox(mwidget)
        self.appproc.setMinimumHeight(300)
        self.appproc.setMinimumWidth(200)
        
        lmwidget = QtGui.QHBoxLayout()
        lmwidget.addWidget(buttonsw)
        lmwidget.addWidget(self.appac)
        lmwidget.addWidget(self.appproc)
        
        mwidget.setLayout(lmwidget)
        
        ###############################
        ## Buttons
        ###############################
        
        acqbtn = QtGui.QPushButton("Acquisition",buttonsw)
        procbtn = QtGui.QPushButton("Processing",buttonsw)
        
        lbuttons= QtGui.QVBoxLayout()
        lbuttons.addWidget(acqbtn)
        lbuttons.addWidget(procbtn)
        lbuttons.addStretch(1)
        
        buttonsw.setLayout(lbuttons)
        
        ##########################
        ## Applications
        ##########################
        layoutac= QtGui.QVBoxLayout()
        self.measurebtn = AppIcon("../../SistemaMedicion/images/measuresys.ico","System Measurement")
        layoutac.addWidget(self.measurebtn)
        
        layoutproc = QtGui.QVBoxLayout()
        self.analyzerbtn = AppIcon("../../AnalysisData/images/analyzer2.ico","Analyzer Waveform")
        self.extractorbtn = AppIcon("../../ISFET/images/parameter2.ico","Parameter Extractor")
        layoutproc.addWidget(self.analyzerbtn)
        layoutproc.addWidget(self.extractorbtn)
        
        self.appac.setLayout(layoutac)
        self.appproc.setLayout(layoutproc)
        
        self.appproc.hide()
        ############################
        ##Connect btns
        ############################
        acqbtn.clicked.connect(self.changelayout)
        procbtn.clicked.connect(self.changelayout)
        
    def changelayout(self):
        
        sender = self.sender()
        if sender.text() == "Acquisition":
            self.appproc.hide()
            self.appac.show()
            
        elif sender.text() == "Processing":
            self.appac.hide()
            self.appproc.show()
            
            
class AppIcon(QtGui.QWidget):
    
    def __init__(self,iconfile,title,parent=None):
        super(AppIcon,self).__init__()
        
        self.iconfile = iconfile
        self.title = title
        self.initGUI()
        
    def initGUI(self):
        
        layout = QtGui.QHBoxLayout()
        
        pixmap = QtGui.QPixmap(self.iconfile)
        pixmap = pixmap.scaled(80,80)
        qicon = QtGui.QIcon(pixmap)
        
        self.iconbtn = QtGui.QPushButton(qicon,'')
        #http://stackoverflow.com/a/3146720
        self.iconbtn.setIconSize(pixmap.rect().size())
        self.iconbtn.setFixedSize(80,80)
        
#        title= "System Measurement"
        string ='<span style="font-size:10pt; font-weight: bold;font-style: italic">{title}</span>'
        
        string = string.format(title=self.title)
        
        label = QtGui.QLabel(string)
        label.setMaximumWidth(150)
        #http://stackoverflow.com/a/12281629
        label.setWordWrap(True)
        
        layout.addStretch(1)
        layout.addWidget(self.iconbtn,QtCore.Qt.AlignRight)
        layout.addWidget(label,QtCore.Qt.AlignLeft)
        layout.addStretch(1)
        
        self.setLayout(layout)
        
if __name__=="__main__":
    
    app = QtGui.QApplication([])
    mw = GUI()
    mw.show()
    sys.exit(app.exec_())