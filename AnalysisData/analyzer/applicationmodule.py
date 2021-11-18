# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 19:50:43 2016

@author: lviton

========================
Application Module
========================
Where all the modules are placed

"""
import sys
from PyQt4 import QtGui

import guimodule as gm
import processdata as pd
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class Application(QtGui.QApplication):
    
    def __init__(self):
        super(Application,self).__init__([])
        
        self.initComponents()
        self.connectModules()
        
        sys.exit(self.exec_())
    def initComponents(self):
        
        ##Defining the components
        self.gui = gm.GUI()
        
    def connectModules(self):
        fileselector = self.gui.fileselector
#        visualizer = self.gui.visualizer
        graphicsel = self.gui.graphicsel
        analyzerdock = self.gui.adock
        
        fileselector.loadbtn.clicked.connect(self.loadfiles)
        graphicsel.combo.currentIndexChanged.connect(self.changeplot)
        analyzerdock.highribbon.valueselected.connect(self.changeselected)
        analyzerdock.highribbon.valuechanged.connect(self.updateplot)
        
        self.gui.exportAction.triggered.connect(self.exportdata)
        
        
    def loadfiles(self):
        fileselector = self.gui.fileselector
        visualizer = self.gui.visualizer
        graphicsel = self.gui.graphicsel
        
        fileselector.getFileNames()
        
        if fileselector.filenames != []:
            
            self.ldp =[]
#            try:
            for filename in fileselector.filenames:
                dps = pd.DataProcessor(filename)
                self.ldp = self.ldp +[dps]
                logging.debug( str(filename) + " Correctly added")
            
            fileselector.getBasenames()
            fileselector.setInfo(str(len(self.ldp)),str(len(self.ldp)))
            visualizer.clearPlot()
            visualizer.plotProcessedData(self.ldp,fileselector.basenames)
            visualizer.canvas.draw()
            graphicsel.changeItems(fileselector.basenames)
                
#            except:
#                logging.debug("File error")
            
            self.gui.openAnalizerDock(self.ldp[0])
    
    def changeplot(self,index):
        self.gui.adock.resetPlot()
        self.gui.adock.setProcessor(self.ldp[index])
        
    def changeselected(self,sel):
        graphicsel = self.gui.graphicsel
        idx = graphicsel.combo.currentIndex()
        visualizer = self.gui.visualizer
        logging.debug(str(idx))
        
        visualizer.changeDotPosition(self.ldp[idx],sel)
    
    def updateplot(self,sel):
        fileselector = self.gui.fileselector
        graphicsel = self.gui.graphicsel
        idx = graphicsel.combo.currentIndex()
        visualizer = self.gui.visualizer
        
        visualizer.updatePlot(self.ldp,fileselector.basenames,idx,sel)
        
    def exportdata(self):
        dialog = self.gui.exportdialog
        fileselector = self.gui.fileselector
        try:
            dialog.loadData(fileselector.basenames)
        except:
            QtGui.QMessageBox.critical(dialog,"Export error",'You need to load files first')
            return
        
        dialog.preview.clicked.connect(self.openpreview)
        dialog.export.clicked.connect(self.savefile)
        
        dialog.show()
        
    def openpreview(self):
        dialog = self.gui.exportdialog
        
        dialog.generatePreview(self.ldp)
        
    def savefile(self):
        dialog = self.gui.exportdialog
        
        dialog.exportFile(self.ldp)
        
if __name__ == "__main__":
    app = Application()