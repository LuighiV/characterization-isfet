# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 19:00:47 2016

@author: lviton

========================
Analyzer Contents MW
========================

Describes the main window whre resides the contents

Based on:
    *paramterscontestmw by the author
"""

import sys
from PyQt4 import QtGui,QtCore

import analyzermw as amw
import visualizerplot as vp
import fileselector as fs
import analyzerdock as ad
import graphicselector as gs
import exportdialogv3 as ed

class AnalyzerContentsMW(amw.AnalyzerMW):
    
    def __init__(self):
        super(AnalyzerContentsMW,self).__init__()
        
        self.initContents()
        
    def initContents(self):
        
        ##Defining the main components
        cw= QtGui.QWidget()
        self.fileselector = fs.FileSelector()
        self.visualizer=vp.VisualizerPlot()
        self.graphicsel = gs.GraphicSelector()
        
        self.adock = ad.AnalyzerDock()
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.adock)
        self.viewMenu.addAction(self.adock.toggleViewAction())
        self.adock.hide()
        
        lmain = QtGui.QVBoxLayout()
        lmain.addWidget(self.fileselector)
        lmain.addWidget(self.visualizer)
        lmain.addWidget(self.graphicsel)
        
        cw.setLayout(lmain)
        
        self.setCentralWidget(cw)
        
        ##Adding export action
        #Actions in file menu
        self.exportAction = QtGui.QAction('E&xport...',self)
        self.exportAction.setShortcut('Ctrl+E')
        self.exportAction.setStatusTip('Export data obtained from meausrements')
        
        self.fileMenu.addAction(self.exportAction)
        
        self.exportAction.triggered.connect(self.openexportdialog)
    
    def openAnalizerDock(self,processor):
        self.adock.resetPlot()
        self.adock.setProcessor(processor)
        self.adock.show()
        
    def openexportdialog(self):
        self.exportdialog = ed.ExportDialog()
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw= AnalyzerContentsMW()
    mw.show()
    
    sys.exit(app.exec_())
    
