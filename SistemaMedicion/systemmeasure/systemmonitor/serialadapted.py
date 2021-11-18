# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:42:41 2016

@author: lviton
"""
import sys
sys.path.append("../")
import serialmodule as sm
import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    

class SerialAdapted(sm.SerialModule):
    """
    Class to provide the object of serial Module
    """
    def __init__(self,parent=None):
        """
        Constructor of the class
        """
#        super(SerialAdapter,self).__init__() # is for the new style class
        
        sm.SerialModule.__init__(self)
        
        self.temp = 0
        self.tempntc = 0
        
        self.voltph = 0
        self.phvalue = 0
        
    
    def updateTempData(self,string):
        try:
            data = string.strip()
            if data.find(':') >=0:
                data = data[data.find(':')+1 :]
                sdata = data.split(',')
                self.temp = float(sdata[0])
                self.tempntc = float(sdata[1])
                self.voltph = float(sdata[2])
                self.phvalue = float(sdata[3])
            
        except:
            self.temp = self.temp
            self.tempntc = self.tempntc
            self.voltph = self.voltph
            self.phvalue = self.phvalue
        
    def readTempNumbers(self):
        self.connect()
        data = self.startReading()
        self.updateTempData(data[:-1])
        self.close()
    
    def threadTempRead(self,start,liveplot,livevoltplot,livephplot,recording):
        """
        This provide a function to read in a thread
        """
        while not start.isSet():
            logging.debug("Waiting start event")
        
        while (start.isSet()):
            self.lock.acquire()
            try:
                
                self.readTempNumbers()
                
#                liveplot.appendData(self.temp,self.tempntc)
                liveplot.extendQueue([self.temp],[self.tempntc])
                livevoltplot.extendQueue([self.voltph])
                livephplot.extendQueue([self.phvalue])
                
                if recording.writedata:
                    recording.recordTempData(self.temp,self.tempntc,self.voltph,self.phvalue)
                    
            finally:
                self.lock.release()
        
        logging.debug("Thread finished")

if __name__ == "__main__":
    
    sh = SerialAdapted()
    sh.setPort('COM8')
    
    while (True):
        sh.readTempNumbers()
        print str(sh.temp) + ', ' + str(sh.tempntc) + ', ' + str(sh.voltph) +', ' + str(sh.phvalue)