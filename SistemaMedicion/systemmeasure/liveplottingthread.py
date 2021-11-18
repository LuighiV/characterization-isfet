# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 19:37:36 2016

@author: lviton

=======================================
Live Plotting Thread
=======================================

Description
------------
Plot data acquired via pyqtgraph

References
-----------
Based on 
    Example Plotwidget from pyqtgraph
    Example imageAnalysis from pyqtgraph
    Example crosshair from pyqtgraph
"""
import sys
import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui, QtCore
import serialmodule as sm
import threading
from collections import deque
#import time # Only used in test
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class LivePlotting(pg.PlotWidget):
    """"
    Class to generate a live plot in the widget
    """
    def __init__(self,parent=None):
        super(LivePlotting,self).__init__()
        
        self.p1 = self.plot()
        self.p1.setPen((200,200,100)) #yellow
        
        self.p2= self.plot()
        self.p2.setPen((100,200,100)) #green
        
        ##Used in static plot
        self.t = np.arange(0,100,1)
        self.x1 = np.zeros(100)
        self.x2 = np.zeros(100)
        
        ##Used in dinamic plot
        self.te = np.arange(0,1000,1)
        self.xe1 = np.zeros(1000)
        self.xe2 = np.zeros(1000)

        self.colx = deque()
        self.coly = deque()
        
        # Draggable line for setting isocurve level
        self.isoLine = pg.InfiniteLine(angle=90, movable=True, pen=pg.mkPen(color='c',width=4))
        self.addItem(self.isoLine)
        #self.setMouseEnabled(y=False) # makes user interaction a little easier
        self.isoLine.setValue(100)
        self.isoLine.setBounds([self.te[0],self.te[-1]])
        self.isoLine.sigDragged.connect(self.updatelabel)
        
        #Label in the plot
        self.label = pg.TextItem()
        self.addItem(self.label)
        
        self.getPlotItem().sigYRangeChanged.connect(self.updatelabel)
        #**********************************
        ##Used in serial communication
        #**********************************
#        self.sh = sm.SerialModule()
#        self.sh.setPort('COM8')
    def updatelabel(self):
        index  = int(self.isoLine.value())
        self.label.setHtml("<span style='color: yellow'>x1=%0.1f</span>,<span style='color: #64C864'>x2=%0.1f</span>" % (self.xe1[index], self.xe2[index]))
#        self.label.setPos(index,self.xe1[index])
        
        plot = self.getPlotItem()
        l =plot.getViewBox().viewRange()
#        print l
        self.label.setPos(index,l[1][1])
    #######################################################
    ##Functions used to static view, only updates the plot
    #######################################################
    def appendData(self,x1,x2):
        self.x1 = np.append(self.x1[1:],[x1])
        self.x2 = np.append(self.x2[1:],[x2])
    
    def updateData(self):
        
#        self.sh.readNumbers()
#        print str(self.sh.x) + ', ' + str(self.sh.y)
#        
#        self.appendData(self.sh.x,self.sh.y)
        
        self.p1.clear()
        self.p2.clear()
        
        self.p1.setData(y=self.x1,x=self.t)
        self.p2.setData(y=self.x2,x=self.t)
        
    ############################################################
    ##Functions used to dinamic view, update each actual data
    ############################################################
    def appendLiveData(self,x1,x2):
        self.xe1 = np.append(self.xe1[1:],[x1])
        self.xe2 = np.append(self.xe2[1:],[x2])
    
    def extendQueue(self,l1,l2):
        self.colx.extend(l1)
        self.coly.extend(l2)
        
    def updateLiveData(self):
        
        self.p1.clear()
        self.p2.clear()
        
        try:
            valuex = self.colx.popleft()
            valuey = self.coly.popleft()
            
            self.appendLiveData(valuex,valuey)
            self.p1.setData(y=self.xe1,x=self.te)
            self.p2.setData(y=self.xe2,x=self.te)
            
        except:
            self.p1.setData(y=self.xe1,x=self.te)
            self.p2.setData(y=self.xe2,x=self.te)
        
        self.updatelabel()
    #******************************************************
    #Functions used to test purtposes
    #******************************************************
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

    def threadserial(self):
#        self.r = 0
#        
#        while (True):
#            print(self.r)
#            self.r+=1
#            time.sleep(2)
        self.sh = sm.SerialModule()
        self.sh.setPort('COM8')
        
        while(True):
            self.sh.readStreamNumbers()
            print str(self.sh.x) + ', ' + str(self.sh.y)
            self.appendData(self.sh.x,self.sh.y)
    
    
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
    
    d = threading.Thread(name="threadserial",target=pw.threadserial)
    d.start()
    #pw.plotTest()
    ## Start a timer to rapidly update the plot in pw
    t = QtCore.QTimer()
    #t.timeout.connect(pw.updateDataTest)
    t.timeout.connect(pw.updateData)
    t.start(10)
    #updateData()
    
    
    sys.exit(app.exec_())