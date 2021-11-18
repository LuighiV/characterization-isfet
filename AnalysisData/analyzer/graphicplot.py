# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 23:05:09 2016

@author: luighi

based on:
    *http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies
    *http://stackoverflow.com/questions/10082299/qvboxlayout-how-to-vertically-align-widgets-to-the-top-instead-of-the-center
    *Expand plot: http://stackoverflow.com/a/6377406
"""

import sys
from PyQt4 import QtGui,QtCore

import matplotlib.figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

class GraphicPlot(QtGui.QWidget):
    """
    Set the widget to plot with matplotlib
    """    
    def __init__(self,paren=None):
        super(GraphicPlot,self).__init__()
        
        self.initGUI()
        
    def initGUI(self):
        
        #instance of plot
        self.figure = matplotlib.figure.Figure()
        
        #Display the figure
        self.canvas = FigureCanvas(self.figure)
        #Add functionality to expand the widget
        #http://stackoverflow.com/a/29163409
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                      QtGui.QSizePolicy.Expanding)
        
        self.canvas.updateGeometry()
        
        self.toolbar= NavigationToolbar(self.canvas,self)
        
        ######################################
        ##Main layout
        #####################################
        lmain = QtGui.QVBoxLayout()
        lmain.addWidget(self.toolbar)
        lmain.addWidget(self.canvas)
        
        
        self.setLayout(lmain)
    
    def plotData(self,data):
        
        self.figure.clf()
        ax1 = self.figure.add_subplot(111)
        ax1.plot(data)
        #self.figure.show()
        #self.cursor = wd.Cursor(ax1)
    
    def clearPlot(self):
        self.figure.clf()
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    
    w = GraphicPlot()
    mw.setCentralWidget(w)
    #w.setGeometry(100, 100, 800, 600)
    
    
    
    x= range(10)
    w.plotData(x)
    mw.show()
    
    sys.exit(app.exec_())
