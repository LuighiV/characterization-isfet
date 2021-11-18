# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:06:06 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui

import editorplot as ep

class EditorDock(QtGui.QDialog):
    
    def __init__(self,processor,selected):
        super(EditorDock,self).__init__()
        
        self.processor = None
        self.selected = None
        self.initGUI()
        
    def setProcessorSelected(self,processor,selected):
        self.processor = processor
        self.selected = selected
        
        self.editor = ep.EditorPlot(self.processor,self.selected)
        
        self.editor.plotRaw()
        self.editor.plotFiltered()
        self.editor.plotMean()
        
        ###################################################
        ## Establishing the connections
        ###################################################
        self.rawbtn.stateChanged.connect(self.changerawplot)
        self.filterbtn.stateChanged.connect(self.changefilteredplot)
        
        self.resetbtn.clicked.connect(self.resetplot)
        self.acceptbtn.clicked.connect(self.acceptdialog)
        self.cancelbtn.clicked.connect(self.reject)
        
    def initGUI(self):
        
        ##Definig main components
        controlview = QtGui.QGroupBox("Visualization Control")
        
        controlbuttons = QtGui.QWidget()
        
        ##Add to the main layout
        lmain= QtGui.QVBoxLayout()
        lmain.addWidget(controlview)
        lmain.addWidget(self.editor)
        lmain.addWidget(controlbuttons)
        
        self.setLayout(lmain)
        
        ## Defining control view
        self.rawbtn = QtGui.QCheckBox("Raw Data")
        self.filterbtn = QtGui.QCheckBox("Filtered Data")
        
        self.rawbtn.setChecked(True)
        self.filterbtn.setChecked(True)
        
        lview = QtGui.QHBoxLayout()
        lview.addWidget(self.rawbtn)
        lview.addWidget(self.filterbtn)
        controlview.setLayout(lview)
        
        ##Defining control buttons
        self.resetbtn = QtGui.QPushButton("Reset")
        self.acceptbtn = QtGui.QPushButton("Accept")
        self.cancelbtn = QtGui.QPushButton("Cancel")
        
        lbuttons = QtGui.QHBoxLayout()
        lbuttons.addWidget(self.resetbtn)
        lbuttons.addWidget(self.acceptbtn)
        lbuttons.addWidget(self.cancelbtn)
        
        controlbuttons.setLayout(lbuttons)
        
    def changerawplot(self, state):
        
        if state ==0:
            self.editor.hideRaw()
            self.editor.canvas.draw()
        elif state ==2:
            self.editor.showRaw()
            self.editor.canvas.draw()
    
    def changefilteredplot(self,state):
        
        if state ==0:
            self.editor.hideFiltered()
            self.editor.canvas.draw()
        elif state ==2:
            self.editor.showFiltered()
            self.editor.canvas.draw()
    
    def resetplot(self):
        
        self.editor.resetPlot()
        self.editor.canvas.draw()
        self.rawbtn.setChecked(True)
        self.filterbtn.setChecked(True)
    
    def acceptdialog(self):
        self.data = (self.editor.hline1.get_ydata()[0],self.editor.hline2.get_ydata()[0])
        self.accept()