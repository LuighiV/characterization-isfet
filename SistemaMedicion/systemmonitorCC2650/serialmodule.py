# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:14:33 2016

@author: lviton

==================================================
Serial Module
==================================================

Description
---------------
Module used to manage the serial communication

References
---------------
    Reading ports based on:
        http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        by Thomas
    Logging
        https://pymotw.com/2/threading/
"""

import serial
import sys
import glob
import logging
import threading

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    
class SerialModule:
    """
    Class to provide the object of serial Module
    """
    def __init__(self):
        """
        Constructor of the class
        """
        #Defining the internal variables
        self.__ser=serial.Serial()
        self.__ser.baudrate=115200
        self.__ser.bytesize=8
        self.__ser.stopbits=serial.STOPBITS_ONE
        self.__ser.timeout=0
        
        #Defining the internal data
        self.x = 0
        self.y = 0
        self.streamx = []
        self.streamy = []
        self.dac= 0
        self.timer = 0
        self.control=1
        
        #Defining elements for threading
        self.lock = threading.Lock()
    
    def inWaiting(self):
        data= self.__ser.inWaiting()
        return data
        
    ###################################################
    ##Functions derived from implementation of serial
    ##################################################
    def setPort(self,port):
        """Setting the port name"""
        self.__ser.port=port
        
    def connect(self):
        """Connecting to the port selected"""
        try:
            if(self.__ser.isOpen()==False):
                self.__ser.open()
        except:
            print "Couldn't open serial port"
        
    def close (self):
        """Closing the port """
        if(self.__ser.isOpen()==True):
            self.__ser.close()
        
    def read(self,nbytes):
        """Reading a number of bytes"""
        data= self.__ser.read(nbytes)
        return data
        
    def startReading(self):
        """Reading lines"""
        data = self.__ser.readline()
        logging.debug( "line:" +data[:-1])
        return data
        
    def write (self,data):
        """writing some data"""
        self.__ser.write(data)
        
    ########################################################
    ##Additional features 
    ########################################################
    def readData(self):
        """
        Read data from the port with readline
        """
        self.connect()
        data = self.startReading()
        self.close()
        return data
        
    def writeData(self,data):
        """
        Write the specified data to the port
        """
        self.connect()
        self.write(data)
        self.close()
    
    #################################################################
    ##Functions oriented to process the data
    #################################################################
    def updateNumbers(self,string):
        """
        Function oriented to process data from serial port
        
        Version1:
        try:
            numbers= string.split(',')
            #print numbers
            xnew = int(numbers[0])
            ynew = int(numbers[1])
            self.x = xnew
            self.y = ynew
        except:
            self.x = self.x
            self.y = self.y
        
        """
        try:
            numbers= string.split(':')
            self.dac=int(numbers[1])
            adc = numbers[0].split(',')
            xnew = int(adc[0])
            ynew = int(adc[1])
            self.x = xnew
            self.y = ynew
            
#            print self.x, self.y, self.dac
        except:
            self.x = self.x
            self.y = self.y
            self.dac = self.dac
    
    def updateStreamNumbers(self,string):
        try:
            data = string.strip()
            data = data[data.find(':')+1 :]
            sdata = data.split('#')
            self.dac = int(sdata[1])
            self.timer = int(sdata[2])
            self.control = int(sdata[3])
            
            self.streamx = []
            self.streamy = []
            
            for adcdata in sdata[0].split(':'):
                numbers = adcdata.split(',')
                self.streamx = self.streamx + [int(numbers[0])]
                self.streamy = self.streamy + [int(numbers[1])]
            
            self.x = sum(self.streamx)/len(self.streamx)
            self.y = sum(self.streamy)/len(self.streamy)
        except:
            self.streamx = [self.streamx[-1]]
            self.streamy = [self.streamy[-1]]
            self.x = self.x
            self.y = self.y
        
    def readNumbers(self):
        self.connect()
        data = self.startReading()
        self.updateNumbers(data[:-1])
        self.close()
    
    def readStreamNumbers(self):
        self.connect()
        data = self.startReading()
        self.updateStreamNumbers(data[:-1])
        self.close()
    #######################################################
    ##Functions to work with modules
    #######################################################
    def settings(self,connection):
        acqdata = connection.data
        logging.debug("Acquired data: "+ ','.join(map(str,acqdata)))
        try:
            self.__ser.port = str(acqdata[0])
            self.__ser.baudrate = int(acqdata[1])
            self.__ser.bytesize = int(acqdata[2])
            logging.debug("Setting connection successfully")
            return True
        except:
            logging.debug("Couldn't set the connection")
            return False
    
    def threadWrite(self,start,controldac):
        """
        This provide the function to write via serial in a thread
        """
        while not start.isSet():
            logging.debug("Waiting start event")
        
        while (start.isSet()):
            self.lock.acquire()
            try:
                if controldac.sendItem==1:
                    self.connect()
                    self.write("nn\n")
                    logging.debug("Next message sent")
                    controldac.sendItem=0
                    
                elif controldac.sendItem==2:
                    self.connect()
                    self.write("pp\n")
                    logging.debug("Previous message sent")
                    controldac.sendItem=0
                
                elif controldac.sendItem==3:
                    self.connect()
                    self.write("mm\n")
                    logging.debug("Manual message sent")
                    controldac.sendItem=0
                
                elif controldac.sendItem==4:
                    self.connect()
                    self.write("aa\n")
                    logging.debug("Automactic message sent")
                    controldac.sendItem=0
            finally:
                self.lock.release()
        
        logging.debug("Thread finished")
        
    def threadRead(self,start,controldac,liveplot,recording):
        """
        This provide a function to read in a thread
        """
        while not start.isSet():
            logging.debug("Waiting start event")
        
        while (start.isSet()):
            self.lock.acquire()
            try:
                
                if controldac.sendItem==0:
                    self.readStreamNumbers()
                    controldac.setInfo(self.dac,self.timer,self.control)
                    liveplot.appendData(self.x,self.y)
                    liveplot.extendQueue(self.streamx,self.streamy)
                    
                    if recording.writedata:
                        recording.recordData(self.streamx,self.streamy)
            finally:
                self.lock.release()
        
        logging.debug("Thread finished")
        
####################################################################
##Function to read serial ports: Work in Linux, OS and Windows
###################################################################
def scanPorts():
    """ 
    Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    ##Detects windows platform
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    ##Detects linux platforms
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    ##Detects Mac OS X platforms
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
    
if __name__ == "__main__":
    
    import serialmodule as sm
    
    sh = sm.SerialModule()
    sh.setPort('COM8')
    
    x = 0
    y = 0
    
    while (True):
        sh.readStreamNumbers()
        print str(sh.x) + ', ' + str(sh.y)
        print sh.streamx
        print sh.streamy

