# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 14:00:39 2016

@author: lviton (Luighi Anthony Viton Zorrilla)

================================
Control Module Thread
================================

Description
--------------
Control Module for DAC using threads

"""

from PyQt4 import QtGui
import sys
import serialmodule as sm
import threading
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )

class ControlDACModule(QtGui.QGroupBox):
    """
    Class to control DAC
    """
    def __init__(self,parent=None,serial=None):
        """
        Constructor for the class
        """
        super(ControlDACModule,self).__init__("Control module")
        
        self.sendItem =0
        self.initGUI()
        self.timer = 0
        self.control = 1
        #****************************************************
        #For test purposes
        #****************************************************
        self.sh = serial #Serial module
#        self.sh.setPort('COM8') # Its initialized later in the thread
#        self.e = threading.Event() # Attempt with events. Doesn't work
        
        self.lock = threading.Lock() # lock to share resources
        
    def initGUI(self):
        """
        Initialize graphical elements
        """
        ############################################
        ##Defining the radio buttons
        ############################################
        self.radiobtn1 = QtGui.QRadioButton('Manual',self)
        self.radiobtn2 = QtGui.QRadioButton('Automatic',self)
        self.radiobtn1.setChecked(True)
        
        #Actions
        self.radiobtn1.clicked.connect(self.activecontrol)
        self.radiobtn2.clicked.connect(self.activecontrol)
        
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
        lselection.addWidget(self.radiobtn1)
        lselection.addWidget(self.radiobtn2)
        selection.setLayout(lselection)
        
        ###########################################
        ##Manual group
        ##########################################
        nb = QtGui.QPushButton('Next',self)
        nb.setToolTip('Next value in DAC')
        
        pb = QtGui.QPushButton('Prev',self)
        pb.setToolTip('Previous value in DAC')
        
        self.info = QtGui.QLabel()
        self.info.setText(str(0))
        
        lmanual.addStretch(.5)
        lmanual.addWidget(pb)
        lmanual.addStretch(.1)
        lmanual.addWidget(self.info)
        lmanual.addStretch(.1)
        lmanual.addWidget(nb)
        lmanual.addStretch(.5)
        
        self.manual.setLayout(lmanual)
        
        #Actions connected to buttons
        nb.clicked.connect(self.cbclicked)
        pb.clicked.connect(self.cbclicked)
        
        ############################################
        ##Automatic group
        ############################################
        self.progb=QtGui.QProgressBar(self)
        self.progb.setRange(0,10)
        self.progb.setFormat("%vs")
        #progb.resize(100,10) #This doesn't work
        #self.progb.setValue(50) # Actually it doesn't have a practical purpose
        
        lautomatic.addWidget(self.progb)
        self.automatic.setLayout(lautomatic)
        
        ###########################################
        #set layout in maingroup
        ###########################################
        mglayout =QtGui.QVBoxLayout()
        mglayout.addWidget(selection)
        mglayout.addWidget(self.manual)
        mglayout.addWidget(self.automatic)
        self.setLayout(mglayout)
        
        #btngroup.buttonClicked.connect(self.activecontrol) #I couldn't make this to work
    
    #####################################################
    ## Functions connected to events
    #####################################################
    def cbclicked(self):
        """
        Define the funtion when the button Next or Prev is pressed
        """
        sender = self.sender()
        
        if sender.text() == "Next":
            self.sendItem=1
            
        elif sender.text() == "Prev":
            self.sendItem=2
            
            
    def activecontrol(self):
        """
        Define the function when automatic or manual is pressed
        """
        sender = self.sender()
        if sender.text() == "Manual":
#            self.manual.setEnabled(True)
#            self.automatic.setDisabled(True)
#            self.progb.reset()
            self.sendItem=3
            
        elif sender.text() == "Automatic":
#            self.manual.setDisabled(True)
#            self.automatic.setEnabled(True)
            self.sendItem=4
    
    ###########################################################
    ##Functions to work with modules
    ############################################################
    def setInfo(self,data,timer,control):
        strdata = str(data)
        self.info.setText(strdata + " (" + toVoltage(strdata) + ")")
        self.timer = toSeconds(timer)
        self.control = control
        
    def updateTimer(self):
        self.progb.setValue(self.timer)
    
    def updateMode(self):
        if (self.control==1):
            self.manual.setEnabled(True)
            self.automatic.setDisabled(True)
            self.radiobtn1.setChecked(True)
#            self.progb.reset()
        else:
            self.manual.setDisabled(True)
            self.automatic.setEnabled(True)
            self.radiobtn2.setChecked(True)
    #***********************************************************
    ##Functions for test purposes. Allow work in standalone
    #***********************************************************
    def threadserial(self):
        """
        This provide the function to write via serial in a thread
        """
        while (True):
            self.lock.acquire()
            try:
                if self.sendItem==1:
                    self.sh.connect()
                    self.sh.write("nn\n")
                    self.sendItem=0
                    
                elif self.sendItem==2:
                    self.sh.connect()
                    self.sh.write("pp\n")
                    self.sendItem=0
                
                elif self.sendItem==3:
                    self.sh.connect()
                    self.sh.write("mm\n")
                    self.sendItem=0
                
                elif self.sendItem==4:
                    self.sh.connect()
                    self.sh.write("aa\n")
                    self.sendItem=0
            finally:
                self.lock.release()
                
    def threadread(self):
        """
        This provide a function to read in a thread
        """
        while (True):
            self.lock.acquire()
            try:
                
                if self.sendItem==0:
                    self.sh.connect()
                    data= self.sh.readData()
                    self.info.setText(data)
            finally:
                self.lock.release()

def toVoltage(data):
    """
    This function converts the Data From DAC to voltage
    """
    try:
        number = int(data)
        if number<5:
            voltage=0.0451
        else:
            voltage = number*0.011454 -0.009496
        
        return '{:.3}'.format(voltage) + "V"
    except:
        return "- V"

def toSeconds(data):
    """
    This function converts in seconds
    """
    try:
        number = float(data)
        time = int((number/57600)*10) ##Beacuse the factor in TIM6
        
        return time
    except:
        return 0
    
class ControlButtons (QtGui.QGroupBox):
    """
    This class create buttons to control the process
    """
    def __init__(self,parent=None):
        super(ControlButtons,self).__init__("Control Buttons")
        
        self.initGUI()
        self.start = 0
    def initGUI(self):
        
        ######################################
        ## Defining main elements
        #######################################
        self.pbutton = QtGui.QPushButton("Play",self)
        self.sbutton = QtGui.QPushButton("Stop",self)
        
        self.pbutton.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        self.sbutton.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaStop))
        
        self.pbutton.clicked.connect(self.startprocess)
        self.sbutton.clicked.connect(self.stopprocess)
        
        lmain = QtGui.QHBoxLayout()
        lmain.addWidget(self.pbutton)
        lmain.addWidget(self.sbutton)
        self.setLayout(lmain)
        
    def startprocess(self):
        self.start = 1
        logging.debug("Start process")
    
    def stopprocess (self):
        self.start = 0
        logging.debug("Stop process")

if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    sh = sm.SerialModule()
    sh.setPort('COM8')
    
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Control Widget')
    mw.resize(400,200)
    
    cw = ControlDACModule(serial=sh)
    cb = ControlButtons()
    
    mw.setCentralWidget(cw)
    
    mw.show()
    
    d = threading.Thread(name="threaread",target=cw.threadread)
    d.start()
#    
    d2 = threading.Thread(name="threadserial",target=cw.threadserial)
    d2.start()
    
    sys.exit(app.exec_())