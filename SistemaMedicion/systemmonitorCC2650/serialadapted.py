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
        
        #registrotemporal
        self.temp = ''        
        
        self.tempntc = 0
        self.phvalue = 0
        self.address = ''
        self.onport = ''
        self.fromport = ''
        self.length = ''        
    
    def updateTempData(self,string):
        try:
            print string
            
            self.streamx = []
            self.streamy = []
            
            
            self.address,self.onport,self.fromport,self.length,sdata = tockenString(string)
            sdata = sdata[sdata.find(':')+1:sdata.rfind(':')]
            for adcdata in sdata.split(':'):
                numbers = adcdata.split(',')
                print numbers
                if len(numbers)>=2:
                    self.streamx = self.streamx + [float(numbers[0])]
                    self.streamy = self.streamy + [float(numbers[1])]
            
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
                    print "Received data"
                    print data
                    #mode1
#                    print data
#                    self.updateTempData(data[-1])
#                    liveplot.extendQueue(self.streamx)
#                    livephplot.extendQueue(self.streamy)
#                
#                    if recording.writedata:
#                        recording.recordData(self.streamx,self.streamy)
                    
                    #mode2
                    self.temp = self.temp +data
                    data,self.temp=processBuffer(self.temp)
                    print "Processed data"
                    print data
                    if data != "":
                        self.updateTempData(data)
                        liveplot.extendQueue(self.streamx)
                        livephplot.extendQueue(self.streamy)
                    
                        if recording.writedata:
                            recording.recordData(self.streamx,self.streamy)
                    
            finally:
                self.lock.release()
        
        logging.debug("Thread finished")

def tockenString(string):
    """
        Get data from CC2650 and divide in information about
        Info about port and address of sender, length and data:
        
        Structure is:
            Data received from %s on port %d from port %d 
            with length %d: '%s'\n
            
    """
    string = string.strip()
    tockendata = 'Data received from'
    tockenon = 'on port'
    tockenfrom = 'from port'
    tockenlength = 'with length'
    
    idata = string.find(tockendata)
    ion = string.find(tockenon)
    ifrom = string.find(tockenfrom)
    ilength = string.find(tockenlength)
    
    address = string[idata+len(tockendata):ion].strip()
    onport = string[ion+len(tockenon):ifrom].strip()
    fromport = string[ifrom+len(tockenfrom):ilength].strip()
    length =string[ilength+len(tockenlength):string.find("'")-2].strip()
    data =  string[string.find("'")+1:string.rfind("'")].strip()
    
    return address, onport, fromport, length, data

def processBuffer(buff):
    
    if buff.rfind('\n') != -1:
        lind= buff.rfind('\n')
        
        temp = buff[:lind]
        buff = buff[lind+1:]
        
        find = temp.rfind('Data')
        data = temp[find:]
        
        return data,buff
    else:
        return "",buff
        
if __name__ == "__main__":
    
    sh = SerialAdapted()
    sh.setPort('COM8')
    
    #Test readnumbers
#    while (True):
#        sh.readTempNumbers()
#        print str(sh.tempntc) + ', ' + str(sh.phvalue)
    
    #tockenstring
    
    string = "Data received from fe80::212:4b00:7bb:2183 on port 1234 from port 1234 with length 480: '34.26,22.7:34.26,22.5:34.26,22.7:34.26,22.8:34.26,22.5:34.26,22.4:34.26,22.8:34.26,22.6:34.26,22.7:34.26,23.0:34.26,22.5:34.26,22.6:34.26,22.5:34.26,22.4:34.26,22.5:34.26,22.6:34.26,22.5:34.26,22.5:34.26,22.6:34.26,22.5:34.26,22.8:34.26,22.5:34.26,22.5:34.26,22.4:34.26,22.5:34.26,22.4:34.26,22.7:34.26,22.4:34.26,22.5:34.26,22.5:34.26,22.5:34.26,22.6:34.26,23.0:34.26,22.8:34.26,22.5:34.26,22.8:34.26,22.5:34.26,22.5:34.26,22.4:34.26,22.4:34.26,22.7:34.26,22.6:34.26,22.6:34.26,2'"
    address, onport, fromport, length, data = tockenString(string)