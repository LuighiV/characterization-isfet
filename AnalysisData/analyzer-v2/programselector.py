# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 14:31:15 2017

@author: lviton
"""
import sys
from PyQt4 import QtGui,QtCore
import applicationmodule as appm
import applicationmodulev2 as appmv2
import applicationmodulev3 as appmv3


class AppSelector(QtGui.QApplication):
    
    def __init__(self,parent=None):
        super(AppSelector,self).__init__([])
        
        self.initGUI()
        self.setConnections()
        self.mainw.show()
        sys.exit(self.exec_())
        
    def initGUI(self):
        
        self.mainw = QtGui.QDialog()
        self.mainw.setWindowTitle("Program Selector")
        
        vdsgroup = QtGui.QGroupBox('Vds-ids')
        vgsgroup = QtGui.QGroupBox('Vgs-ids')
        
        
        
        lmain = QtGui.QHBoxLayout()
        lmain.addWidget(vdsgroup)
        lmain.addWidget(vgsgroup)
        self.mainw.setLayout(lmain)
        
        self.vdspga = QtGui.QPushButton('Vds-ids curve\n (with PGA)')
        self. vdsnpga =QtGui.QPushButton('Vds-ids curve\n (without PGA)')
        
        self.vdspga.setFixedWidth(150)
        self.vdsnpga.setFixedWidth(150)
        
        vdslayout = QtGui.QVBoxLayout()
        vdslayout.addWidget(self.vdspga)
        vdslayout.addWidget(self.vdsnpga)
        vdsgroup.setLayout(vdslayout)
        
        self.vgs =QtGui.QPushButton('Vgs-ids curve')
        self.vgs.setFixedWidth(150)
        
        vgslayout = QtGui.QVBoxLayout()
        vgslayout.addWidget(self.vgs)
        vgsgroup.setLayout(vgslayout)
        
    def setConnections(self):
        
        self.vdspga.clicked.connect(self.openvdspga)
        self.vdsnpga.clicked.connect(self.openvdsnpga)
        self.vgs.clicked.connect(self.openvgs)
        
    def openvdspga(self):
        
        psm = "python applicationmodule.py"
        self.process  = QtCore.QProcess()
        self.process.start(psm)
        
        self.mainw.hide()
    
    def openvdsnpga(self):
        
        psm = "python applicationmodulev2.py"
        self.process  = QtCore.QProcess()
        self.process.start(psm)
        
        self.mainw.hide()
    
    def openvgs(self):
        
        psm = "python applicationmodulev3.py"
        self.process  = QtCore.QProcess()
        self.process.start(psm)
        
        self.mainw.hide()
    
if __name__ == "__main__":
    
    app = AppSelector()