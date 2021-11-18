# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 11:23:00 2016

@author: lviton

Based on:
    *http://zetcode.com/gui/pyqt4/menusandtoolbars/
    *http://zetcode.com/gui/pyqt4/firstprograms/
    *http://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot

"""

from PyQt4 import QtGui, QtCore
import sys

class MeasureMainW(QtGui.QMainWindow):
    """
        Define the main window used for the application
    """
    def __init__(self,parent=None):
        super(MeasureMainW,self).__init__()
        
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
        fileMenu = menubar.addMenu('&File')
        toolMenu = menubar.addMenu('&Tools')
        helpMenu = menubar.addMenu('&Help')
        
        #Actions in file menu
        exitAction = QtGui.QAction(QtGui.QIcon('../images/close.png'),'&Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(exitAction)
        
        #Actions in tools menu
        showAction = QtGui.QAction('Status bar',self)
        showAction.setShortcut('Ctrl+1')
        showAction.setStatusTip('Toggle status bar')
        showAction.setCheckable(True)
        showAction.setChecked(True)
        showAction.toggled.connect(lambda: self.togglestatusbar(showAction))
        
        viewMenu= toolMenu.addMenu('View')
        viewMenu.addAction(showAction)
        
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
        self.setWindowTitle('Measurement Toolkit')
        self.setWindowIcon(QtGui.QIcon('../images/measuresys.png'))
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
    
    mmw=MeasureMainW()
    
    sys.exit(app.exec_())
