# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 20:22:25 2016

@author: lviton (Luighi Anthony Viton Zorrilla)

=========================
Measurement Main Contents
=========================

Description
-----------
Inherited from measurementmainw, set the main componentes in the window

"""
import sys
from PyQt4 import QtGui

import connectionmodule as cm
import controlmodulethread  as ctrmth
import measuremainw as mmw
import liveplottingthread as lvpltth
import measurements as ms
import recording as rec

class MeasureMainContents(mmw.MeasureMainW):
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
        super(MeasureMainContents,self).__init__()
        
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
        self.controldac = ctrmth.ControlDACModule()
        self.controlbtn = ctrmth.ControlButtons()
        self.recording = rec.RecordingWidget()
        
        lcontrols= QtGui.QVBoxLayout()
        lcontrols.addWidget(self.settings)
        lcontrols.addWidget(self.controlbtn)
        lcontrols.addWidget(self.controldac)
        lcontrols.addWidget(self.recording)
        groupcontrols.setLayout(lcontrols)
        groupcontrols.setMaximumWidth(300)
        
        #######################################
        ##Group view
        #######################################
        self.liveplot = lvpltth.LivePlotting()
        self.measurements = ms.MeasurementView(self.liveplot)
        
        self.liveplot.setMinimumWidth(500)
        
        lview = QtGui.QHBoxLayout()
        lview.addWidget(self.liveplot)
        lview.addWidget(self.measurements)
        groupview.setLayout(lview)
        
if __name__ =="__main__":
    
    app = QtGui.QApplication([])
    
    mw = MeasureMainContents()
    mw.show()
    
    sys.exit(app.exec_())