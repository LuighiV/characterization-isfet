# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:25:31 2016

@author: lviton

=========================
Monitor Main Contents
=========================

Description
-----------
Inherited from measurementmainw, set the main componentes in the window

"""
import sys
from PyQt4 import QtGui
#sys.path.append("../")
import connectionmodule as cm
import controlmodulethread  as ctrmth
import measuremainw as mmw
import livecustomplotting as lvcplt
import monitorview as ms
import recordingtemp as rec

class MonitorMainContents(mmw.MeasureMainW):
    """
    MeasureMainContents
    -------------------
    Insert all elemnents in the same window
    
    Methods:
        `__init()`
        `initGUIContents()`
    """
    def __init__(self,parent=None):
        """
        Contructor of MeasureMainContents
        """
        super(MonitorMainContents,self).__init__()
        
        self.initGUIContents()
        
    def initGUIContents(self):
        """
        Create the componentes in the MainWindow
        Those componentes are:
            1.ConnectionModule
            2.ControlModule
            3.ControlButtons
            4.LivePlotting
            
        The  main layout is divided in two groups
            1.GroupControls: connection, control 
            2.GroupView: liveplotting
        """
        ######################################
        ##Define the main layout
        #######################################
        cw = QtGui.QWidget()
        lmain = QtGui.QHBoxLayout()
        groupcontrols = QtGui.QWidget()
        groupview = QtGui.QWidget()
        lmain.addWidget(groupcontrols)
        lmain.addWidget(groupview)
        cw.setLayout(lmain)
        self.setCentralWidget(cw)
        
        #######################################
        ##Group Controls
        ######################################
        self.settings = cm.ConnectionModule()
        self.controlbtn = ctrmth.ControlButtons()
        self.recording = rec.RecordingWidget()
        
        lcontrols= QtGui.QVBoxLayout()
        lcontrols.addWidget(self.settings)
        lcontrols.addWidget(self.controlbtn)
        lcontrols.addWidget(self.recording)
        groupcontrols.setLayout(lcontrols)
        groupcontrols.setMaximumWidth(300)
        
        #######################################
        ##Group view
        #######################################
        self.livetempplot = lvcplt.LiveOnePlotting()
        self.livephplot = lvcplt.LiveOnePlotting()
        self.measurements = ms.MonitorOneView(self.livetempplot,'ISFET')
        self.measureph = ms.MonitorOneView(self.livephplot,'NTC')
        
        self.livetempplot.setMinimumWidth(500)
        
        lview = QtGui.QGridLayout()
        lview.addWidget(self.livetempplot,0,0)
        lview.addWidget(self.measurements,0,1)
        lview.addWidget(self.livephplot,1,0)
        lview.addWidget(self.measureph,1,1)
        groupview.setLayout(lview)
        
if __name__ =="__main__":
    
    app = QtGui.QApplication([])
    
    mw = MonitorMainContents()
    mw.show()
    
    sys.exit(app.exec_())
