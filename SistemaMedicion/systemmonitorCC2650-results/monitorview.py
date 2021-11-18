# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 16:52:52 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )

class MonitorTwoView(QtGui.QGroupBox):
    
    def __init__(self,liveplot,labels,parent=None):
        super(MonitorTwoView,self).__init__("Measurements")
        self.liveplot = liveplot
        self.labels=labels
        self.initGUI()
    
    def initGUI(self):
        
        self.list= []
        self.list.append(MonitorValue(label=self.labels[0]))
        self.list.append(MonitorValue(label=self.labels[1]))
        
        lmain = QtGui.QVBoxLayout()
        
        for widget in self.list:
            lmain.addWidget(widget)
        
        lmain.addStretch(1)
        
        self.setLayout(lmain)
    
    def updateData(self):
        self.list[0].updateData(self.liveplot.xe1)
        self.list[1].updateData(self.liveplot.xe2)

class MonitorOneView(QtGui.QGroupBox):
    
    def __init__(self,liveplot,variable,parent=None):
        super(MonitorOneView,self).__init__("Measurements")
        self.liveplot = liveplot
        self.label = variable
        self.initGUI()
    
    def initGUI(self):
        
        self.list= []
        self.list.append(MonitorValue(label=self.label))
        
        lmain = QtGui.QVBoxLayout()
        
        for widget in self.list:
            lmain.addWidget(widget)
        
        lmain.addStretch(1)
        
        self.setLayout(lmain)
    
    def updateData(self):
        self.list[0].updateData(self.liveplot.xe1)
        
class MonitorValue(QtGui.QWidget):
    
    def __init__(self,label,parent=None):
        super(MonitorValue,self).__init__()
        self.label = label
        self.initGUI()
    
    def initGUI(self):
        
        self.title = QtGui.QLabel(self.label)
        self.value = QtGui.QLabel()
        
        self.value.setMinimumWidth(80)
        
        self.value.setAlignment(QtCore.Qt.AlignRight)
        
        lmain = QtGui.QGridLayout()
        lmain.addWidget(self.title,0,0)
        lmain.addWidget(self.value,0,1)
        
        self.setLayout(lmain)
    
    def updateData(self,value):
        "Update data depending type of value"
        ##Check if value es int
        if type(value)== int or type(value)== float:
            self.value.setText( str(value))
        ##Check if value is list
        elif type(value) == list or type(value) == np.ndarray:
            mean = self.calcMean(value[-10:])
            self.value.setText(str(mean))
        else:
            logging.debug("Provided an incorrect value type" + str(type(value)))
        
    def calcMean(self,lista):
        return float(sum(lista)/len(lista))