# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:58:43 2016

@author: lviton
"""
import sys
from PyQt4 import QtGui,QtCore
import guimodule as gm

class Launcher(QtGui.QApplication):
    
    def __init__(self,parent=None):
        super(Launcher,self).__init__([])
        
        self.initGUI()
        self.connectApps()
        self.processes = []
        sys.exit(self.exec_())
        
    def initGUI(self):
        
        self.gui = gm.GUI()
        
    def connectApps(self):
        measurebtn = self.gui.measurebtn
        analyzerbtn = self.gui.analyzerbtn
        extractorbtn = self.gui.extractorbtn
        
        measurebtn.iconbtn.clicked.connect(self.openmeasure)
        analyzerbtn.iconbtn.clicked.connect(self.openanalyzer)
        extractorbtn.iconbtn.clicked.connect(self.openextractor)
        
    def openmeasure(self):
        psm = "python ../../SistemaMedicion/systemmeasure/applicationmodule.py"
        process  = QtCore.QProcess()
        process.start(psm)
        self.processes.append(process)
        
    def openanalyzer(self):
        paw = "python ../../AnalysisData/analyzer/applicationmodule.py"
        process  = QtCore.QProcess()
        process.start(paw)
        self.processes.append(process)
        
    def openextractor(self):
        ppe = "python ../../ISFET/parameters/applicationmodule.py"
        process  = QtCore.QProcess()
        process.start(ppe)
        self.processes.append(process)
        
if __name__ == "__main__":
    
    app = Launcher()
