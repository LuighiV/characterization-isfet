# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 19:35:13 2016

@author: lviton
"""
import sys
from PyQt4 import QtGui
import analyzercontentsmw as acmw

class GUI(acmw.AnalyzerContentsMW):
    
    def __init__(self):
        super(GUI,self).__init__()
        

if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    mw = GUI()
    mw.show()
    sys.exit(app.exec_())