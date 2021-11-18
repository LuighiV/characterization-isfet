# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 19:57:47 2016

@author: lviton

based on:
    *http://zetcode.com/gui/pyqt4/layoutmanagement/
    *http://electronics.stackexchange.com/questions/9264/what-standard-uart-rates-are-there
"""

from PyQt4 import QtGui
import serialmodule as sm

import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class ConnectionModule(QtGui.QGroupBox):
    """
    Widget for serial connection
    """
    
    def __init__(self,parent=None):
        super(ConnectionModule,self).__init__("Connection module")
        
        self.initGUI()
        self.data = []
        
    def initGUI(self):
        """
        Initialize graphical elements
        """
        ############################################
        ##Defining the main components
        ############################################
        serialLabel = QtGui.QLabel("Serial")
        buttonsettings = QtGui.QPushButton("Settings",self)
        
        self.sdialog = SettingsDialog()
        buttonsettings.clicked.connect(self.openSettingsDialog)
        
        self.sdialog.accepted.connect(self.changevalues)
        
        ###########################################
        #set layout in maingroup
        ###########################################
        mglayout =QtGui.QHBoxLayout()
        mglayout.addWidget(serialLabel)
        mglayout.addWidget(buttonsettings)
        self.setLayout(mglayout)

    def openSettingsDialog(self):
        self.sdialog.exec_()
    
    def changevalues (self):
        self.data = self.sdialog.data
        logging.debug( ','.join(map(str,self.data)))

class SettingsDialog(QtGui.QDialog):
    """
    Dialog to configure settings
    """
    def __init__(self,parent=None):
        super(SettingsDialog,self).__init__()
        
        self.initGUI()
        
        
    def initGUI(self):
        self.setWindowTitle("Connection settings")
        
        lmain= QtGui.QVBoxLayout()
        maingroup=QtGui.QWidget()
        scangroup= QtGui.QWidget()
        btngroup = QtGui.QWidget()
        
        lmain.addWidget(scangroup)
        lmain.addWidget(maingroup)
        lmain.addWidget(btngroup)
        
        ####################################
        ##Set main group
        ###################################
        grid= QtGui.QGridLayout()
        maingroup.setLayout(grid)
        
        port = QtGui.QLabel('Port:')
        baudrate = QtGui.QLabel('Baud rate:')
        bytesize = QtGui.QLabel('Byte size:')
        
        self.portEdit = QtGui.QComboBox()
        #self.portEdit.setDuplicatesEnabled(False) Even allow duplicated items via program
        self.portEdit.activated[int].connect(self.porteditactive)
        
        self.baudrateEdit = QtGui.QComboBox()
        self.baudrateEdit.insertItems(1,['9600','19200','38400','57600','115200 '])
        self.bytesizeEdit = QtGui.QComboBox()
        self.bytesizeEdit.insertItems(1,['8','10','12'])
        
        ####################################
        #Adding to layout
        ####################################
        
        grid.addWidget(port,1,0)
        grid.addWidget(self.portEdit,1,1)
        
        grid.addWidget(baudrate,2,0)
        grid.addWidget(self.baudrateEdit,2,1)
        
        grid.addWidget(bytesize,3,0)
        grid.addWidget(self.bytesizeEdit,3,1)
        
        ####################################
        ##Button group
        ####################################
        btnlayout = QtGui.QHBoxLayout()
        btngroup.setLayout(btnlayout)
        
        self.btnaccept = QtGui.QPushButton("Ok",self)
        btncancel = QtGui.QPushButton("Cancel",self)
        
        self.btnaccept.setDisabled(True)
       
        
        self.btnaccept.clicked.connect(self.acceptDialog)
        btncancel.clicked.connect(self.rejectDialog)
        
        btnlayout.addWidget(self.btnaccept)
        btnlayout.addWidget(btncancel)
        
        ####################################
        ##Scan group
        ####################################
        scanlayout = QtGui.QHBoxLayout()
        scangroup.setLayout(scanlayout)
        
        btnscan = QtGui.QPushButton("Scan ports",self)
        btnscan.clicked.connect(self.scanports)
        
        scanlayout.addWidget(btnscan)
        
        self.setLayout(lmain)
    
    def porteditactive(self,index):
        self.btnaccept.setEnabled(True)
        logging.debug("Change is active")
        
    def acceptDialog(self):
        self.data = [self.portEdit.currentText(),
                         self.baudrateEdit.currentText(),
                         self.bytesizeEdit.currentText()]
        self.accept()
    
    def rejectDialog(self):
        self.reject()
        
    def scanports(self):
        
        listports = sm.scanPorts()
        self.portEdit.clear()
        self.portEdit.insertItems(1,listports)
        
if __name__=="__main__":
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Control Widget')
    mw.resize(200,200)
    
    cw = ConnectionModule()
    mw.setCentralWidget(cw)
    
    mw.show()