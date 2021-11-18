# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 15:16:18 2016

@author: lviton

Based on Exmaple Plotwidget from pyqtgraph
"""
import sys
import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui, QtCore
import serialmodule as sm

class LivePlotting(pg.PlotWidget):
    
    def __init__(self,parent=None):
        super(LivePlotting,self).__init__()
        
        self.p1 = self.plot()
        self.p1.setPen((200,200,100))
        
        self.p2= self.plot()
        self.p2.setPen((100,200,100))
        
        self.t = np.arange(0,100,1)
        self.x1 = np.zeros(100)
        self.x2 = np.zeros(100)
        
        """
        Para comunicacion serial
        """
        self.sh = sm.SerialModule()
        self.sh.setPort('COM8')
    
    def appendData(self,x1,x2):
        self.x1 = np.append(self.x1[1:],[x1])
        self.x2 = np.append(self.x2[1:],[x2])
    
    def updateData(self):
        
        self.sh.readNumbers()
        print str(self.sh.x) + ', ' + str(self.sh.y)
        
        self.appendData(self.sh.x,self.sh.y)
        
        self.p1.clear()
        self.p2.clear()
        
        self.p1.setData(y=self.x1,x=self.t)
        self.p2.setData(y=self.x2,x=self.t)
    """
     Funciones para test de live plotting
    """
    def plotTest(self):
        self.x = np.arange(0,100,.01)
        self.y = np.sin(self.x/5)
        self.z = np.cos(self.x/5)
        self.p1.setData(y=self.y,x=self.x)
        self.p2.setData(y=self.z,x=self.x)
    
    def updateDataTest(self):
        self.x = self.x+.5
        self.y = np.sin(self.x/5)
        self.z = np.cos(self.x/5)
        self.p1.setData(y=self.y,x=self.x)
        self.p2.setData(y=self.z,x=self.x)

def main():
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('PlotWidget')
    mw.resize(800,400)
    
    cw = QtGui.QWidget()
    mw.setCentralWidget(cw)
    
    l = QtGui.QVBoxLayout()
    cw.setLayout(l)
    
    pw=LivePlotting()
    l.addWidget(pw)
    
    pw.plotTest()
    ## Start a timer to rapidly update the plot in pw
    t = QtCore.QTimer()
    t.timeout.connect(pw.updateDataTest)
    t.start(20)
    #updateData()

    mw.show()
    sys.exit(app.exec_())
    

if __name__== "__main__":
    
    
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('PlotWidget')
    mw.resize(800,400)
    
    cw = QtGui.QWidget()
    mw.setCentralWidget(cw)
    
    l = QtGui.QVBoxLayout()
    cw.setLayout(l)
    
    pw=LivePlotting()
    l.addWidget(pw)
    
    mw.show()
    #pw.plotTest()
    ## Start a timer to rapidly update the plot in pw
    t = QtCore.QTimer()
    #t.timeout.connect(pw.updateDataTest)
    t.timeout.connect(pw.updateData)
    t.start(20)
    #updateData()
    
    
    sys.exit(app.exec_())