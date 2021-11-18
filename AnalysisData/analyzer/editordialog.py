# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:55:35 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui

import editorplot2 as ep

class EditorDialog(QtGui.QDialog):
    
    def __init__(self,processor,selected):
        super(EditorDialog,self).__init__()
        
        self.processor = processor
        self.selected = selected
        self.initGUI()
        
    def initGUI(self):
        
        ##Setting the title
        self.setWindowTitle("EditorDialog")
        
        ##Definig main components
        controlview = QtGui.QGroupBox("Visualization Control")
        self.editor = ep.EditorPlot(self.processor,self.selected)
        controlbuttons = QtGui.QWidget()
        
        self.editor.plotRaw()
        self.editor.plotFiltered()
        self.editor.plotMean()
        
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
        resetbtn = QtGui.QPushButton("Reset")
        acceptbtn = QtGui.QPushButton("Accept")
        cancelbtn = QtGui.QPushButton("Cancel")
        
        lbuttons = QtGui.QHBoxLayout()
        lbuttons.addWidget(resetbtn)
        lbuttons.addWidget(acceptbtn)
        lbuttons.addWidget(cancelbtn)
        
        controlbuttons.setLayout(lbuttons)
        
        ###################################################
        ## Establishing the connections
        ###################################################
        self.rawbtn.stateChanged.connect(self.changerawplot)
        self.filterbtn.stateChanged.connect(self.changefilteredplot)
        
        resetbtn.clicked.connect(self.resetplot)
        acceptbtn.clicked.connect(self.acceptdialog)
        cancelbtn.clicked.connect(self.reject)
        
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

def newEditorDialog(processor,selected):
    dialog = EditorDialog(processor,selected)
    retval = dialog.exec_()
    
    if retval == 1:
        return dialog.data
    else:
        return None
        
if __name__ == "__main__":
    
    import processdata as pd
    
    dps = pd.DataProcessor('prueba750mV.txt')
    
    app = QtGui.QApplication([])
    
    retval = newEditorDialog(dps,12)
    
    print retval
    
    sys.exit(app.exec_())