# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 10:12:23 2016

@author: lviton
"""


import sys
from PyQt4 import QtGui

import analyzerplot as ap

class AnalyzerDock(QtGui.QDockWidget):
    
    def __init__(self):
        super(AnalyzerDock,self).__init__("Analyzer dock")
        
        self.processor = None
        self.initGUI()
        
    def setProcessor(self,processor):
        self.processor=processor
        
        self.analyzer.plotRaw(self.processor)
        self.analyzer.plotFiltered(self.processor)
        self.analyzer.plotMask(self.processor)
        self.analyzer.canvas.draw()
        
        self.highribbon.setProcessor(self.processor,self.analyzer.ax)
        self.highribbon.connect()
        
        
        
    def initGUI(self):
        
        ##Definig main components
        controlview = QtGui.QGroupBox("Visualization Control")
        
        ## Defining control view
        self.rawbtn = QtGui.QCheckBox("Raw Data")
        self.filterbtn = QtGui.QCheckBox("Filtered Data")
        self.maskbtn = QtGui.QCheckBox("Mask")
        self.meanbtn = QtGui.QCheckBox("Mean")
        
        self.rawbtn.setChecked(True)
        self.filterbtn.setChecked(True)
        self.maskbtn.setChecked(True)
        self.meanbtn.setChecked(True)
        
        lview = QtGui.QHBoxLayout()
        lview.addWidget(self.rawbtn)
        lview.addWidget(self.filterbtn)
        lview.addWidget(self.maskbtn)
        lview.addWidget(self.meanbtn)
        controlview.setLayout(lview)
        
        ##Adding the analyzerplot
        self.analyzer = ap.AnalyzerPlot()
        self.highribbon = ap.HighLightRibbon()
        
        ##Add to the main layout
        main = QtGui.QWidget()
        lmain= QtGui.QVBoxLayout()
        lmain.addWidget(controlview)
        lmain.addWidget(self.analyzer)
        
        main.setLayout(lmain)
        self.setWidget(main)
        
        ###################################################
        ## Establishing the connections
        ###################################################
        self.rawbtn.stateChanged.connect(self.changerawplot)
        self.filterbtn.stateChanged.connect(self.changefilteredplot)
        self.maskbtn.stateChanged.connect(self.changemaskplot)
        
    def changerawplot(self,state):
        if self.analyzer.raw:
            if state ==0:
                self.analyzer.hideRaw()
                self.analyzer.canvas.draw()
            elif state ==2:
                self.analyzer.showRaw()
                self.analyzer.canvas.draw()
    
    def changefilteredplot(self,state):
        if self.analyzer.filtered:
            if state ==0:
                self.analyzer.hideFiltered()
                self.analyzer.canvas.draw()
            elif state ==2:
                self.analyzer.showFiltered()
                self.analyzer.canvas.draw()
    
    def changemaskplot(self,state):
        if self.analyzer.mask:
            if state ==0:
                self.analyzer.hideMask()
                self.analyzer.canvas.draw()
            elif state ==2:
                self.analyzer.showMask()
                self.analyzer.canvas.draw()
    
    def resetPlot(self):
        self.analyzer.resetPlot()
        if self.highribbon.connected:
            self.highribbon.disconnect()
            
if __name__ == "__main__":
    import processdata as pd
    
    dps = pd.DataProcessor('prueba750mV.txt')
    
    app = QtGui.QApplication([])
    
    ad = AnalyzerDock()
    ad.setProcessor(dps)
    ad.show()
    
    ad.resetPlot()
    ad.setProcessor(dps)
    
    sys.exit(app.exec_())
    