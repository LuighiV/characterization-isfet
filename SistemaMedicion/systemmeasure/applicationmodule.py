# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 17:44:16 2016

@author: lviton

=======================
Application
=======================

Description
-----------------------
Main application which contains the GUI and the serial module
"""

import sys
from PyQt4 import QtGui,QtCore

import guimodule as gm
import serialmodule as sm
import threading

class Application(QtGui.QApplication):
    """
    Class contains the GUI and serial module
    """
    def __init__(self,parent=None):
        super(Application,self).__init__([])
        
        self.dataconnection = []
        self.senditem = 0
        self.numbers = []
        self.start = 0
        self.initComponents()
        self.connectModules()
        sys.exit(self.exec_())
        
    def initComponents(self):
        
        self.gui = gm.GUI()
        self.serial =sm.SerialModule ()
        
    def connectModules(self):
        ##Connecting the settings
        sdialog = self.gui.settings.sdialog
        sdialog.accepted.connect(self.changeserial)
        
        ##Connecting play and stop buttons
        playbtn = self.gui.controlbtn.pbutton
        stopbtn = self.gui.controlbtn.sbutton
        
        playbtn.clicked.connect(self.startprocess)
        stopbtn.clicked.connect(self.stopprocess)
        
    ####################################################
    ##ethod to connect modules 
    ####################################################
    def changeserial(self):
        serial = self.serial
        sdialog = self.gui.settings.sdialog
        serial.settings(sdialog)
    
    def startprocess(self):
        serial= self.serial
        controldac = self.gui.controldac
        liveplot= self.gui.liveplot
        measurements= self.gui.measurements
        recording = self.gui.recording
        
        ##Thread to serial module
        self.start = threading.Event()
        
        d = threading.Thread(name="threadwrite",
                                 target=serial.threadWrite,
                                 args=(self.start,controldac))
        d.start()
        
        d2 = threading.Thread(name="threadread",
                                  target=serial.threadRead,
                                  args=(self.start,controldac,liveplot,recording))
        d2.start()
        
        self.start.set()
        
        ##Updating the plot in liveplot
        self.t = QtCore.QTimer()
        self.t.timeout.connect(liveplot.updateLiveData)
        self.t.timeout.connect(measurements.updateData)
        self.t.timeout.connect(controldac.updateMode)
        self.t.timeout.connect(controldac.updateTimer)
        self.t.start(25)
        
    def stopprocess(self):
        self.start.clear()
        
if __name__ == "__main__":
    
    app = Application()
