# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:11:04 2016

@author: lviton Luighi Viton Zorrilla

======================================
Measurements
======================================

Description
---------------
Widget to show data from liveplotting

"""

import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )

class MeasurementView(QtGui.QGroupBox):
    
    def __init__(self,liveplot,parent=None):
        super(MeasurementView,self).__init__("Measurements")
        self.liveplot = liveplot
        
        self.initGUI()
    
    def initGUI(self):
        
        self.list= []
        self.list.append(MeanValue(label="Mean x"))
        self.list.append(MeanValue(label="Mean y"))
        
        lmain = QtGui.QVBoxLayout()
        
        for widget in self.list:
            lmain.addWidget(widget)
        
        lmain.addStretch(1)
        
        self.setLayout(lmain)
    
    def updateData(self):
        self.list[0].updateData(self.liveplot.xe1)
        self.list[1].updateData(self.liveplot.xe2)

class MeanValue(QtGui.QWidget):
    
    def __init__(self,label,parent=None):
        super(MeanValue,self).__init__()
        self.label = label
        self.initGUI()
    
    def initGUI(self):
        
        self.title = QtGui.QLabel(self.label)
        self.value = QtGui.QLabel()
        self.volt = QtGui.QLabel()
        
        self.value.setMinimumWidth(80)
        self.volt.setMinimumWidth(80)
        
        self.value.setAlignment(QtCore.Qt.AlignRight)
        self.volt.setAlignment(QtCore.Qt.AlignRight)
        
        lmain = QtGui.QGridLayout()
        lmain.addWidget(self.title,0,0)
        lmain.addWidget(self.value,0,1)
        lmain.addWidget(self.volt,1,1)
        
        self.setLayout(lmain)
    
    def updateData(self,value):
        "Update data depending type of value"
        ##Check if value es int
        if type(value)== int :
            self.value.setText( str(value))
            self.volt.setText(adcToVoltage(value))
        ##Check if value is list
        elif type(value) == list or type(value) == np.ndarray:
            mean = self.calcMean(value[-100:])
            self.value.setText(str(mean))
            self.volt.setText(adcToVoltage(mean))
        else:
            logging.debug("Provided an incorrect value type" + str(type(value)))
        
    def calcMean(self,lista):
        return int(sum(lista)/len(lista))
        
def adcToVoltage(value):
    voltage = value*0.7162
    return '{:.1f}mV'.format(voltage)
    
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw = MeasurementView(None)
    mw.show()
    sys.exit(app.exec_())
