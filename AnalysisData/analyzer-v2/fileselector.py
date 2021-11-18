# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 19:59:04 2016

@author: lviton
"""
import sys
from PyQt4 import QtGui
import os.path
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )

class FileSelector(QtGui.QWidget):
    
    def __init__(self):
        super(FileSelector,self).__init__()
        
        self.initGUI()
        
    def initGUI(self):
        
        ######################################
        ##Defining Main components
        ######################################
        self.loadbtn = QtGui.QPushButton("Load")
        self.editbtn = QtGui.QPushButton("Edit")
        infogroup = QtGui.QGroupBox("Files info")
        
        infogroup.setMinimumWidth(200)
        
        lmain = QtGui.QHBoxLayout()
        
        
        lmain.addWidget(infogroup)
        lmain.addStretch(1)
        lmain.addWidget(self.loadbtn)
        lmain.addWidget(self.editbtn)
        
        self.setLayout(lmain)
        
        #########################################
        ## info group
        #########################################
        tlabel = QtGui.QLabel("Total:")
        self.total = QtGui.QLabel("-")
        
        vlabel = QtGui.QLabel("View:")
        self.view = QtGui.QLabel("-")
        
        linfo = QtGui.QGridLayout()
        linfo.addWidget(tlabel,1,1)
        linfo.addWidget(self.total, 1,2)
        linfo.addWidget(vlabel, 1,3)
        linfo.addWidget(self.view, 1,4)
        
        infogroup.setLayout(linfo)
        
    def getFileNames(self):
        self.filenames = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', 
                './')
        
        logging.debug(','.join(map(str,self.filenames)))
    

    def getBasenames(self):
        self.basenames = map(os.path.basename,map(str,self.filenames))
        self.basenames = [base.rstrip('.txt') for base in self.basenames]
        logging.debug(','.join(self.basenames))
        
        
    def setInfo(self,total,view):
        self.total.setText(total)
        self.view.setText(view)
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    w = FileSelector()
    w.show()
    
    sys.exit(app.exec_())
        