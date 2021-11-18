# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:21:58 2016

@author: luighi

============================
Analyzer MainW
============================

Defines the main window to be used in the Analyzer

Based on:
    measurementmainw.py by the author
    parametersmw.py by the author
"""

from PyQt4 import QtGui
import sys

class AnalyzerMW(QtGui.QMainWindow):
    
    def __init__(self,parent=None):
        super(AnalyzerMW,self).__init__()
        
        self.initGUI()
        
    def initGUI(self):
        """
         Defining the graphical appearance
        """
        ##########################################
        ##Define the menubar and its elements
        ##########################################
        menubar = self.menuBar()
        #Elements in Menu
        self.fileMenu = menubar.addMenu('&File')
        toolMenu = menubar.addMenu('&Tools')
        helpMenu = menubar.addMenu('&Help')
        
        #Actions in file menu
        exitAction = QtGui.QAction(QtGui.QIcon('../images/close.png'),'&Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        self.fileMenu.addAction(exitAction)
        
        #Actions in tools menu
        showAction = QtGui.QAction('Status bar',self)
        showAction.setShortcut('Ctrl+1')
        showAction.setStatusTip('Toggle status bar')
        showAction.setCheckable(True)
        showAction.setChecked(True)
        showAction.toggled.connect(lambda: self.togglestatusbar(showAction))
        
        self.viewMenu= toolMenu.addMenu('View')
        self.viewMenu.addAction(showAction)
        
        #Actions in help menu
        aboutAction = QtGui.QAction(QtGui.QIcon('../images/help.png'),'&About',self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About the software')
        
        helpMenu.addAction(aboutAction)
        
        ###########################################
        ##Define the statusbar
        ###########################################
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')
        
        ###########################################
        ##Caracteristics of QMainWindow
        ###########################################
        self.setWindowTitle('Analyzer Waveform')
        self.setWindowIcon(QtGui.QIcon('../images/analyzer.png'))
        self.resize(800,400)
        self.show()
    
    def closeEvent(self, event):
        """
        Reimplements closeEvent when try to close the widget
        """
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
    
    def togglestatusbar(self,action):
        """
        Implement method to toggle status bar
        """
        if action.isChecked():
            self.statusbar.show()
        else:
            self.statusbar.hide()
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mmw=AnalyzerMW()
    
    sys.exit(app.exec_())
        
        