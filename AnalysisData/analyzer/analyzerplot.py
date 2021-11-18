# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 17:47:04 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui,QtCore

import graphicplot as gp
import editordialog as ed
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class AnalyzerPlot(gp.GraphicPlot):
    
    def __init__(self):
        super(AnalyzerPlot,self).__init__()
        
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()
        self.raw = False
        self.filtered = False
        self.mask = False
        
    def plotRaw(self,processor):
        data= processor.data
        self.lin1, = self.ax.plot(data.x)
        self.lin2, = self.ax.plot(data.y)
        self.raw=True
    
    def showRaw(self):
        self.lin1.set_visible(True)
        self.lin2.set_visible(True)
    
    def hideRaw(self):
        self.lin1.set_visible(False)
        self.lin2.set_visible(False)
    
    def plotFiltered(self,processor):
        p1 = processor.process1
        p2 = processor.process2
        
        self.new1, = self.ax.plot(p1.newx)
        self.new2, = self.ax.plot(p2.newx)
        
        self.filtered = True
    
    def showFiltered(self):
        self.new1.set_visible(True)
        self.new2.set_visible(True)
        
    def hideFiltered(self):
        self.new1.set_visible(False)
        self.new2.set_visible(False)
    
    def plotMask(self,processor):
        
        l = processor.getRanges(False)
        
        self.ribbons = []
        for item in l:
            ribbon = self.ax.axvspan(item[0], item[1], ymin=0, ymax=1,facecolor='1', alpha=0.5,hatch='/')
            self.ribbons = self.ribbons + [ribbon]
            
        self.mask = True
        
    def showMask(self):
        
        for ribbon in self.ribbons:
            ribbon.set_visible(True)
    
    def hideMask(self):
        
        for ribbon in self.ribbons:
            ribbon.set_visible(False)
    
    def resetPlot(self):
        self.clearPlot()
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()
        self.raw = False
        self.filtered = False
        self.mask = False
        
class HighLightRibbon(QtCore.QObject):
    
    valueselected = QtCore.pyqtSignal(int)
    valuechanged = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super(HighLightRibbon,self).__init__()
        
        self.axes = None
        self.connected = False
        
        self.valueselected.connect(self.signalemitted)
        self.valuechanged.connect(self.signal2emitted)
    
    def signalemitted(self,sel):
        logging.debug("Signal emitted with selection "+ str(sel))
    
    def signal2emitted(self,sel):
        logging.debug("Signal value changed emitted " + str(sel))
        
    def connect(self):
        self.connected = True
        figure = self.axes.figure
        self.me = figure.canvas.mpl_connect("motion_notify_event",self)
        self.bp = figure.canvas.mpl_connect("button_press_event",self)
    
    def disconnect(self):
        figure = self.axes.figure
        figure.canvas.mpl_disconnect(self.me)
        figure.canvas.mpl_disconnect(self.bp)
        self.connected = False
        
    def setProcessor(self,processor,axes):
        self.axes =axes
        self.processor= processor
        self.ranges =processor.getRanges(True)
        
        self.ribbons = []
        for item in self.ranges:
            ribbon = self.axes.axvspan(item[0], item[1], ymin=0, ymax=1,facecolor='0.80', alpha=0.5)
            ribbon.set_visible(False)
            self.ribbons = self.ribbons + [ribbon]
        
    def __call__(self,event):
        x = event.xdata
        
        if x is not None:
            selected = None
            for idx in range(len(self.ranges)):
                if (x >self.ranges[idx][0]) and (x<self.ranges[idx][1]):
                    selected = idx
                    break
            
            for ribbon in self.ribbons:
                ribbon.set_visible(False)
            
            if selected is not None:
                self.valueselected.emit(selected)
                self.ribbons[selected].set_visible(True)
            
            event.canvas.draw()
        
            if event.dblclick and (selected is not None):
                logging.debug("double click")
                self.retval = ed.newEditorDialog(self.processor,selected)
                logging.debug(self.retval)
                
                if self.retval is not None:
                    self.processor.changeAtPoint(selected,self.retval)
                    self.valuechanged.emit(selected)

if __name__ == "__main__":
    import processdata as pd
    
    dps = pd.DataProcessor('prueba750mV.txt')
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    
    ap = AnalyzerPlot()
    mw.setCentralWidget(ap)
    
    ap.plotRaw(dps)
    ap.plotFiltered(dps)
    ap.plotMask(dps)
    
    h =HighLightRibbon()
    h.setProcessor(dps,ap.ax)
    h.connect()
    
    mw.show()
    
    sys.exit(app.exec_())