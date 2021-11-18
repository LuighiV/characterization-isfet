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
        sm.SerialModule.__init__(self)
        
        self.tempntc = 0
        self.phvalue = 0
                
    
    def updateTempData(self,string):
        try:
            print string
            
            self.streamx = []
            self.streamy = []
        
            sdata = string.strip()
            sdata = sdata[sdata.find(':')+1:sdata.rfind(':')]
            for adcdata in sdata.split(':'):
                numbers = adcdata.split(',')
                print numbers
                if len(numbers)>=2:
                    self.streamx = self.streamx + [float(numbers[0])/4.3*7.0]*50
                    self.streamy = self.streamy + [float(numbers[1])]*50
            
            self.tempntc = sum(self.streamx)/len(self.streamx)
            self.phvalue = sum(self.streamy)/len(self.streamy)
            
               
        except:
            self.streamx = self.streamx
            self.streamy = self.streamy
            #self.temp = self.temp
            self.tempntc = self.tempntc
            #self.voltph = self.voltph
            self.phvalue = self.phvalue
            
    
    def threadTempRead(self,start,liveplot,livephplot,recording):
        """
        This provide a function to read in a thread
        """
        while not start.isSet():
            logging.debug("Waiting start event")
        
        while (start.isSet()):
            self.lock.acquire()
            try:
                
                self.connect()
                queue = self.inWaiting()
                if queue >0:
                    data= self.read(8000)
                    self.updateTempData(data[:-1])
                    liveplot.extendQueue(self.streamx)
                    livephplot.extendQueue(self.streamy)
                
                    if recording.writedata:
                        recording.recordData(self.streamx,self.streamy)
                    
            finally:
                self.lock.release()
        
        logging.debug("Thread finished")

if __name__ == "__main__":
    
    sh = SerialAdapted()
    sh.setPort('COM6')
    
    while (True):
        sh.readTempNumbers()
#        print str(sh.tempntc) + ', ' + str(sh.phvalue)
