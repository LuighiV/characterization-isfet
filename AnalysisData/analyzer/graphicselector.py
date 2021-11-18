# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:50:40 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui

class GraphicSelector(QtGui.QGroupBox):
    
    def __init__(self):
        super(GraphicSelector,self).__init__("Graphic Selector")
        
        self.initGUI()
        
    def initGUI(self):
        
        self.combo  = QtGui.QComboBox(self)
        self.prevbtn = QtGui.QPushButton(self)
        self.nextbtn = QtGui.QPushButton(self)
        
        self.combo.setSizeAdjustPolicy(0)
        
        self.prevbtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_ArrowBack))
        self.nextbtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_ArrowForward))
        
        lmain = QtGui.QHBoxLayout()
        lmain.addStretch(1)
        lmain.addWidget(self.prevbtn)
        lmain.addWidget(self.combo)
        lmain.addWidget(self.nextbtn)
        lmain.addStretch(1)
        
        self.setLayout(lmain)
        
        ##Connecting modules
        self.prevbtn.clicked.connect(self.prevvalue)
        self.nextbtn.clicked.connect(self.nextvalue)
    
    def prevvalue(self):
        idx = self.combo.currentIndex()
        if idx > 0:
            self.combo.setCurrentIndex(idx-1)
    
    def nextvalue(self):
        idx = self.combo.currentIndex()
        if idx < self.combo.count()-1:
            self.combo.setCurrentIndex(idx+1)
    
    def changeItems(self,l):
        self.combo.clear()
        self.combo.insertItems(1,l)
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    listports = ['qw','er','wrt']
    w = GraphicSelector()
    w.changeItems(listports)
    w.show()
    
    sys.exit(app.exec_())