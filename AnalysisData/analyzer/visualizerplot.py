# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 18:23:56 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui
import graphicplot as gp
import processdata as pd
import numpy as np
from matplotlib.cm import get_cmap

class VisualizerPlot(gp.GraphicPlot):
    
    def __init__(self):
        super(VisualizerPlot,self).__init__()
        
    def plotProcessedData(self,ldp,basenames):
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Measurements V vs I")
        self.ax.set_xlabel("Voltage (mV)")
        self.ax.set_ylabel("Current (uA)")
        self.ax.grid()
        self.setAxis(ldp)
        #        Color maps: http://stackoverflow.com/a/16006929
        cmap = get_cmap('jet')
        self.colors = [cmap(i) for i in np.linspace(0,1,len(ldp))]
        
        self.plotLines(ldp,basenames)
        self.createDot(ldp)
        self.canvas.draw()
        
    def updatePlot(self,ldp,basenames,index,sel):
        self.clearPlot()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Measurements V vs I")
        self.ax.set_xlabel("Voltage (mV)")
        self.ax.set_ylabel("Current (uA)")
        self.ax.grid()
        self.setAxis(ldp)
        
        self.plotLines(ldp,basenames)
        self.createDot(ldp,index,sel)
        
        self.canvas.draw()
        
    def plotLines(self,ldp,basenames):
        self.lines = []
        for idx in range(len(ldp)):
            l, =self.ax.plot(pd.tomVolts(ldp[idx].volt),pd.touAmpere(ldp[idx].current),'o',label=basenames[idx],color=self.colors[idx])
            self.lines = self.lines + [l]
        
#        http://matplotlib.org/users/legend_guide.html
        self.ax.legend(#bbox_to_anchor=(1.05, 1), 
                       borderaxespad=0.,prop={'size':8},loc='center left', bbox_to_anchor=(1, 0.5))
            
    def createDot(self,ldp,idx = 0, sel = 0):
        ##Printing the dot
        # from :http://matplotlib.org/examples/shapes_and_collections/scatter_demo.html
        area = np.pi * (8)**2
        self.dot = self.ax.scatter(pd.tomVolts(ldp[idx].volt)[sel],pd.touAmpere(ldp[idx].current)[sel],s=area,c='yellow',alpha=0.8)
        self.dot.set_visible(True)
        
    def changeDotPosition(self,process,sel):
        self.dot.set_offsets((pd.tomVolts(process.volt)[sel],pd.touAmpere(process.current)[sel]))
        self.canvas.draw()
        
    def clearPlot(self):
        self.figure.clf()
        
    def setAxis(self,ldp):
        xmin,xmax,ymin,ymax=pd.getLimits(ldp)
        xrang=xmax-xmin
        yrang=ymax-ymin
        self.ax.set_xlim(xmin-.05*xrang,xmax+.05*xrang)
        self.ax.set_ylim(ymin-.05*yrang,ymax+.05*yrang)

if __name__  == "__main__":
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    
    w = VisualizerPlot()
    mw.setCentralWidget(w)
    
    mw.show()
    
    sys.exit(app.exec_())