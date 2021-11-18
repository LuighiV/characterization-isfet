# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:58:02 2016

@author: lviton
"""

import sys
sys.path.append("../")
import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui, QtCore
import serialmodule as sm
import threading
from collections import deque
#import time # Only used in test
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class LiveTwoPlotting(pg.PlotWidget):
    """"
    Class to generate a live plot in the widget
    """
    def __init__(self,parent=None):
        super(LiveTwoPlotting,self).__init__()
        
        self.p1 = self.plot()
        self.p1.setPen((200,200,100)) #yellow
        
        self.p2= self.plot()
        self.p2.setPen((100,200,100)) #green
        
        self.te = np.arange(0,500,1)
        self.xe1 = np.zeros(500)
        self.xe2 = np.zeros(500)

        self.colx = deque()
        self.coly = deque()
        
    ############################################################
    ##Functions used to dinamic view, update each actual data
    ############################################################
    def appendLiveData(self,x1,x2):
        self.xe1 = np.append(self.xe1[1:],[x1])
        self.xe2 = np.append(self.xe2[1:],[x2])
    
    def extendQueue(self,l1,l2):
        self.colx.extend(l1)
        self.coly.extend(l2)
        
    def updateLiveData(self):
        
        self.p1.clear()
        self.p2.clear()
        
        try:
            valuex = self.colx.popleft()
            valuey = self.coly.popleft()
            
            self.appendLiveData(valuex,valuey)
            self.p1.setData(y=self.xe1,x=self.te)
            self.p2.setData(y=self.xe2,x=self.te)
            
        except:
            self.p1.setData(y=self.xe1,x=self.te)
            self.p2.setData(y=self.xe2,x=self.te)
        
class LiveOnePlotting(pg.PlotWidget):
    """"
    Class to generate a live plot in the widget
    """
    def __init__(self,parent=None):
        super(LiveOnePlotting,self).__init__()
        
        self.p1 = self.plot()
        self.p1.setPen((200,200,100)) #yellow
        
        self.te = np.arange(0,500,1)
        self.xe1 = np.zeros(500)

        self.colx = deque()
        
    ############################################################
    ##Functions used to dinamic view, update each actual data
    ############################################################
    def appendLiveData(self,x1):
        self.xe1 = np.append(self.xe1[1:],[x1])
    
    def extendQueue(self,l1):
        self.colx.extend(l1)
        
    def updateLiveData(self):
        self.p1.clear()
        
        try:
            valuex = self.colx.popleft()
            
            self.appendLiveData(valuex)
            self.p1.setData(y=self.xe1,x=self.te)
            
        except:
            self.p1.setData(y=self.xe1,x=self.te)
        