# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:37:57 2016

@author: lviton
"""


import sys
from PyQt4 import QtGui

import analyzerplot as ap

class AnalyzerDialog(QtGui.QDialog):
    
    def __init__(self,processor):
        super(AnalyzerDialog,self).__init__()
        
        self.processor = processor
        self.initGUI()
        
    def initGUI(self):
        
        ##Definig main components
        controlview = QtGui.QGroupBox("Visualization Control")
        self.analyzer = ap.AnalyzerPlot()
        
        self.analyzer.plotRaw(self.processor)
        self.analyzer.plotFiltered(self.processor)
        self.analyzer.plotMask(self.processor)
        
        ap.HighLightRibbon(self.processor,self.analyzer.ax)
        
        ##Add to the main layout
        lmain= QtGui.QVBoxLayout()
        lmain.addWidget(controlview)
        lmain.addWidget(self.analyzer)
        
        self.setLayout(lmain)
        
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
        
        ###################################################
        ## Establishing the connections
        ###################################################
        self.rawbtn.stateChanged.connect(self.changerawplot)
        self.filterbtn.stateChanged.connect(self.changefilteredplot)
        self.maskbtn.stateChanged.connect(self.changemaskplot)
        
    def changerawplot(self,state):
        if state ==0:
            self.analyzer.hideRaw()
            self.analyzer.canvas.draw()
        elif state ==2:
            self.analyzer.showRaw()
            self.analyzer.canvas.draw()
    
    def changefilteredplot(self,state):
        
        if state ==0:
            self.analyzer.hideFiltered()
            self.analyzer.canvas.draw()
        elif state ==2:
            self.analyzer.showFiltered()
            self.analyzer.canvas.draw()
    
    def changemaskplot(self,state):
        if state ==0:
            self.analyzer.hideMask()
            self.analyzer.canvas.draw()
        elif state ==2:
            self.analyzer.showMask()
            self.analyzer.canvas.draw()
            
if __name__ == "__main__":
    import processdata as pd
    
    dps = pd.DataProcessor('prueba750mV.txt')
    
    app = QtGui.QApplication([])
    
    ad = AnalyzerDialog(dps)
    
    ad.show()
    
    sys.exit(app.exec_())
    