# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:52:33 2016

@author: lviton
"""

import sys
from PyQt4 import QtGui, QtCore
import processdata as pd
import os.path

class ExportDialog(QtGui.QDialog):
    
    def __init__(self):
        super(ExportDialog,self).__init__()
        
        self.initGUI()
        
    def initGUI(self):
        
        ##Defining the main components
        self.setWindowTitle("Export Dialog")
        
        selectfile = QtGui.QGroupBox("Select File")
        self.table = QtGui.QTableWidget()
        controlbuttons = QtGui.QWidget()

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["File basename","Output name"])
        
        lmain = QtGui.QVBoxLayout()
        lmain.addWidget(selectfile)
        lmain.addWidget(self.table)
        lmain.addWidget(controlbuttons)
        
        self.setLayout(lmain)
        
        
        ## File selector
        self.filew = QtGui.QLineEdit()
        self.browsebtn = QtGui.QPushButton("Browse")
        
        lselect = QtGui.QHBoxLayout()
        lselect.addWidget(self.filew)
        lselect.addWidget(self.browsebtn)
        
        selectfile.setLayout(lselect)
        
        
        ##Export button
        self.preview = QtGui.QPushButton("Preview")
        self.export = QtGui.QPushButton("Export")
        
        lcontrol = QtGui.QHBoxLayout()
        lcontrol.addWidget(self.preview)
        lcontrol.addStretch(1)
        lcontrol.addWidget(self.export)
        
        controlbuttons.setLayout(lcontrol)
        
        ## Establishing the connections
        self.browsebtn.clicked.connect(self.selectfilename)
    
    def selectfilename(self):
        
        userfilename = QtGui.QFileDialog.getSaveFileName(self,"Save file",'./','Text files (*.txt)')
        
        self.filew.setText(userfilename)
    
    def loadData(self,basenames):
        
        self.table.setRowCount(len(basenames))
        
        for idx in range(len(basenames)):
            baseitem = QtGui.QTableWidgetItem(basenames[idx])
            baseitem.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
            baseitem.setCheckState(QtCore.Qt.Checked)
            self.table.setItem(idx,0,baseitem)
            self.table.setItem(idx,1,QtGui.QTableWidgetItem(''))
    
    def generatePreview(self,ldp):
        preview = QtGui.QTextEdit()
        
        for idx in range(self.table.rowCount()):
            refitem = self.table.item(idx,0)
            
            if refitem.checkState()== QtCore.Qt.Checked:
                item = self.table.item(idx,1)
                process = ldp[idx]
                preview.insertPlainText('vgs\t')
                preview.insertPlainText(item.text())
                preview.insertPlainText('\n\nvds\t ids\n')
                
                for iidx in range(len(process.volt)):
                    volt = pd.tomVolts(process.volt[iidx])
                    current = pd.touAmpere(process.current[iidx])
                    preview.insertPlainText('{:.2f}\t{:.2f}\n'.format(volt,current))
                
                preview.insertPlainText('\n')
                
        dialog = QtGui.QDialog()
        lmain = QtGui.QVBoxLayout()
        lmain.addWidget(preview)
        dialog.setLayout(lmain)
        dialog.exec_()
    
    def exportFile(self,ldp):
        
        try:
            filename = self.filew.text()
            if not os.path.exists(filename):
                
                f = open (filename,'w')
            else:
                retval =  QtGui.QMessageBox.warning(self,"File already exists","Are you sure to replace the file",
                                                        QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel,
                                                        QtGui.QMessageBox.Cancel)
                if retval== QtGui.QMessageBox.Yes:
                    f = open (filename,'w')
                    
                else:
                    self.filew.selectAll()
                    return
        except:
            retval =  QtGui.QMessageBox.information(self,"Invalid filename","Please choose a valid filename")
            return retval
        
        for idx in range(self.table.rowCount()):
            refitem = self.table.item(idx,0)
            
            if refitem.checkState()== QtCore.Qt.Checked:
                item = self.table.item(idx,1)
                process = ldp[idx]
                f.write('vgs\t')
                f.write(item.text())
                f.write('\n\nvds\t ids\n')
                
                for iidx in range(len(process.volt)):
                    volt = pd.tomVolts(process.volt[iidx])
                    current = pd.touAmpere(process.current[iidx])
                    f.write('{:.2f}\t{:.2f}\n'.format(volt,current))
                
                f.write('\n')
        
        f.close()
        
        QtGui.QMessageBox.information(self,"Export finished","File saved succesfully!")
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    w = ExportDialog()
    basenames = ['uno','dos']
    w.loadData(basenames)
    w.show()
    
    
    sys.exit(app.exec_())