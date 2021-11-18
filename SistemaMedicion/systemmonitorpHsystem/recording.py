# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:26:23 2016

@author: lviton
"""
import sys
from PyQt4 import QtGui, QtCore
import shutil
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class RecordingWidget(QtGui.QGroupBox):
    
    def __init__(self,parent=None):
        super(RecordingWidget,self).__init__("Recording Data")
        
        self.initGUI()
        self.f = None
        self.filename = None
        self.writedata = False
        self.count = 0
        
    def initGUI(self):
        
        ######################################
        ##Main elements
        #####################################
        buttons = QtGui.QWidget()
        wstatus = QtGui.QWidget()
        
        lmain = QtGui.QVBoxLayout()
        lmain.addWidget(buttons)
        lmain.addWidget(wstatus)
        
        self.setLayout(lmain)
        
        #######################################
        ##Buttons widget
        ######################################
        self.recordbtn=QtGui.QPushButton("Record")
        self.pausebtn = QtGui.QPushButton("Pause")
        self.stopbtn=QtGui.QPushButton("Finish")
        
        self.recordbtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        self.pausebtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPause))
        self.stopbtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_FileDialogEnd))
        
        ##Set initial state
        self.pausebtn.setDisabled(True)
        self.stopbtn.setDisabled(True)
        
        lbuttons = QtGui.QHBoxLayout()
        lbuttons.addWidget(self.recordbtn)
        lbuttons.addWidget(self.pausebtn)
        lbuttons.addWidget(self.stopbtn)
        
        buttons.setLayout(lbuttons)
        
        #######################################
        ##Status widget
        ######################################
        label = QtGui.QLabel("Status: ")
        self.status = QtGui.QLabel("Stopped")
        
        lstatus = QtGui.QHBoxLayout()
        lstatus.addWidget(label)
        lstatus.addWidget(self.status)
        
        wstatus.setLayout(lstatus)
        
        ########################################
        ##Actions connected
        ########################################
        self.recordbtn.clicked.connect(self.startrecord)
        self.pausebtn.clicked.connect(self.pauserecord)
        self.stopbtn.clicked.connect(self.endrecord)
        
    #######################################################
    ##Functions to work with module serial
    #######################################################
    def startrecord(self):
        self.filename = "temp"+str(self.count)+".tmp"
        self.f = open(self.filename,'w')
        self.writedata = True
        logging.debug("Start writting data ")
        self.setRecording()
    
    def pauserecord(self):
        
        if self.writedata == True:
            self.writedata=False
            self.setPause()
    
        elif self.writedata == False:
            self.writedata=True
            self.setResume()
    
    def endrecord (self):
        self.writedata = False
        logging.debug("Finish writting data ")
        self.f.close()
        self.count+=1
        
        userfilename = QtGui.QFileDialog.getSaveFileName(self,"Save file",'./','Text files (*.txt)')
        shutil.copyfile(self.filename,userfilename)
        
        self.setStop()
        
    def setRecording(self):
        self.recordbtn.setDisabled(True)
        self.pausebtn.setEnabled(True)
        self.stopbtn.setEnabled(True)
        
        self.status.setText("Recording")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.red)

        self.status.setPalette(palette)
        
    def setPause(self):
        self.status.setText("Paused")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.blue)
        
        self.status.setPalette(palette)
        self.pausebtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_BrowserReload))
        self.pausebtn.setText("Resume")
        
    def setResume(self):
        self.status.setText("Recording")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.red)
        
        self.status.setPalette(palette)
        self.pausebtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPause))
        self.pausebtn.setText("Pause")
        
    def setStop(self):
        self.status.setText("Stopped")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.black)
        
        self.status.setPalette(palette)
        
        self.stopbtn.setDisabled(True)
        self.pausebtn.setDisabled(True)
        self.recordbtn.setEnabled(True)
    
    def recordData(self,datax,datay):
        
        if type(datax) == list and type(datay) == list:
            sdatax = map(str,datax)
            sdatay = map(str,datay)
            
            for index in range(min(len(datax),len(datay))):
                self.f.write(', '.join([sdatax[index],sdatay[index]]) + '\n')
            
        elif type(datax) == int and type(datay) == int:
            self.f.write(', '.join([str(datax),str(datay)]) + '\n')
        
        else:
            logging.debug("Provided value not written " + str(type(datax)))
            
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw= RecordingWidget()
    
    mw.show()
    
    sys.exit(app.exec_())