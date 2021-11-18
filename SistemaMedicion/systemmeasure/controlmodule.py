# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 19:12:34 2016

@author: lviton
"""

from PyQt4 import QtGui, QtCore
import sys
import serialmodule as sm
import threading

class ControlModule(QtGui.QWidget):
    
    def __init__(self,parent=None):
        super(ControlModule,self).__init__()
        
        self.number = 0
        self.initGUI()
        
        self.sh = sm.SerialModule()
        self.sh.setPort('COM8')
    
    def initGUI(self):
        """
        Initialize graphical elements
        """
        ############################################
        ## Establishing the main Layout
        ############################################
        maingroup=QtGui.QGroupBox("Control module",self)
        mainlayout = QtGui.QHBoxLayout()
        self.setLayout(mainlayout)
        
        mainlayout.addWidget(maingroup)
        
        ############################################
        ##Defining the radio buttons
        ############################################
        radiobtn1 = QtGui.QRadioButton('Manual',self)
        radiobtn2 = QtGui.QRadioButton('Automatic',self)
        radiobtn1.setChecked(True)
        
        radiobtn1.clicked.connect(self.activecontrol)
        radiobtn2.clicked.connect(self.activecontrol)
        
        ############################################
        ##Group selector
        ###########################################
        selection = QtGui.QWidget()
        self.manual = QtGui.QWidget()
        self.automatic = QtGui.QWidget()
        
        lselection = QtGui.QHBoxLayout()
        lmanual =QtGui.QHBoxLayout()
        lautomatic = QtGui.QHBoxLayout()
        
        ###########################################
        ##selection group
        ###########################################
        lselection.addWidget(radiobtn1)
        lselection.addWidget(radiobtn2)
        selection.setLayout(lselection)
        
        ###########################################
        ##Manual group
        ##########################################
        nb = QtGui.QPushButton('Next',self)
        nb.setToolTip('Next value in DAC')
        
        pb = QtGui.QPushButton('Prev',self)
        pb.setToolTip('Previous value in DAC')
        
        self.info = QtGui.QLabel()
        self.info.setText(str(self.number))
        
        lmanual.addStretch(.5)
        lmanual.addWidget(pb)
        lmanual.addStretch(.1)
        lmanual.addWidget(self.info)
        lmanual.addStretch(.1)
        lmanual.addWidget(nb)
        lmanual.addStretch(.5)
        
        self.manual.setLayout(lmanual)
        #manual.setDisabled(True)
        
        #Actions connected to buttons
        nb.clicked.connect(self.cbClicked)
        pb.clicked.connect(self.cbClicked)
        
        ############################################
        ##Automatic group
        ############################################
        self.progb=QtGui.QProgressBar(self)
        self.progb.setFormat("%vs")
        #progb.resize(100,10)
        self.progb.setValue(50)
        
        lautomatic.addWidget(self.progb)
        self.automatic.setLayout(lautomatic)
        
        ###########################################
        #set layout in maingroup
        ###########################################
        mglayout =QtGui.QVBoxLayout()
        mglayout.addWidget(selection)
        mglayout.addWidget(self.manual)
        mglayout.addWidget(self.automatic)
        maingroup.setLayout(mglayout)
        
        #btngroup.buttonClicked.connect(self.activecontrol)
        
    def cbClicked(self):
        sender = self.sender()
        
        if sender.text() == "Next":
            #self.number +=1
            #self.info.setText(str(self.number))
            self.sh.connect()
            self.sh.write("nn\n")
            data= self.sh.startReading()
            self.sh.close()
            self.info.setText(data[:-1] + ' (' + toVoltage(data[:-1]) +')')
        elif sender.text() == "Prev":
            #self.number -=1
            #self.info.setText(str(self.number))
            self.sh.connect()
            self.sh.write("pp\n")
            data= self.sh.readData()
            self.sh.close()
            self.info.setText(data[:-1] + ' (' + toVoltage(data[:-1]) +')')
    
    def activecontrol(self):
        sender = self.sender()
        if sender.text() == "Manual":
            self.manual.setEnabled(True)
            self.automatic.setDisabled(True)
            
            self.sh.connect()
            self.sh.write("mm\n")
            data= self.sh.startReading()
            self.sh.close()
            self.info.setText(data[:-1] + ' (' + toVoltage(data[:-1]) +')')
            
            self.progb.reset()
        elif sender.text() == "Automatic":
            self.manual.setDisabled(True)
            self.automatic.setEnabled(True)
            
            self.sh.connect()
            self.sh.write("aa\n")
            #data= self.sh.startReading()
            self.sh.close()
            #self.info.setText(data[:-1])
    
    def threadserial(self):
        
        #self.sh.connect()
        
        while(True):
            data= self.sh.readData()
            self.info.setText(data)

def toVoltage(data):
    try:
        number = int(data)
        if number<5:
            voltage=0.0451
        else:
            voltage = number*0.011454 -0.009496
        
        return '{:.3}'.format(voltage) + "V"
    except:
        return "- V"
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Control Widget')
    mw.resize(400,200)
    
    cw = ControlModule()
    mw.setCentralWidget(cw)
    
    mw.show()
    
    #d = threading.Thread(name="threadserial",target=cw.threadserial)
    #d.start()
    
    sys.exit(app.exec_())