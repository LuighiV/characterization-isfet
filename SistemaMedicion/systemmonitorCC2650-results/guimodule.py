# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 17:29:40 2016

@author: lviton
============================
GUI
============================

Description
-----------
The module for the mainwindow

"""

import sys
from PyQt4 import QtGui

import monitormaincontents as mmc 

class GUI(mmc.MonitorMainContents):
    """
    Implementation of GUI Main Window
    """
    def __init__(self,parent=None):
        super(GUI,self).__init__()

if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw = GUI()
    mw.show()
    
    sys.exit(app.exec_())