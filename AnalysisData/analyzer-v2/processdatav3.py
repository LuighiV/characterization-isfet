# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 18:41:25 2016

@author: lviton
"""

import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt
import dataacquire

class SimpleMovingAverage():
    
    def __init__(self,datax):
        
        self.x= datax
        self.newx = []
        
        self.calcValues(50)
    
    def calcValues(self,n):
        init = [self.x[0]]*n
        
        extendx = init+self.x
        
        prev = self.x[0]
        index = 0
        for data in extendx[n:]:
            x = prev + float(data - extendx[index])/n
            index +=1
            self.newx.append(x)
            prev = x

def getDifference(vector):
    x1 = np.asarray(vector)
    forward =  [vector[0]] + vector[:-1] 
    x2 = np.asarray(forward)
#    print x2
    dif = x1-x2
    return dif
    
def getMask(vector):
    pmask = abs(sc.medfilt(map(int,5*getDifference(vector)),5))
    hist, bin_edges= np.histogram(pmask, bins = np.arange(10),density=True)
#    plt.figure()
#    plt.hist(pmask, bins=bin_edges)
    
    mask = pmask >3
    return mask

def getSets(vector,mask):
    nvector= []
    tmp= []
    
    for index in range(len(mask)):
        if mask[index] ==0:
            tmp = tmp +[vector[index]]
        else:
            if tmp != []:
                nvector = nvector + [tmp]
            tmp = []
        
        index+=1
    
    return nvector

def mean(vector):
    return float(sum(vector))/len(vector)

def tomVolts(vector):
    if type(vector) is np.ndarray or list:
        return np.asarray(vector)*0.71620211 -0.09969365
    elif type(vector) is float or int:
        return vector*0.71620211 -0.09969365
    
def touAmpere(vector):
    return tomVolts(vector)/20

class DataProcessor:
    
    def __init__(self,filename):
        self.data = dataacquire.DataAcquisition()
        self.data.setFile(filename)
        self.data.getData()
        self.applyFilter()
        self.getMask()
        self.getSets()
    
    def plotData(self):
        plt.figure()
        plt.plot(sc.medfilt(self.data.x))
        plt.plot(sc.medfilt(self.data.y))
    
    def applyFilter(self):
        self.process1 = SimpleMovingAverage(list(sc.medfilt(self.data.x)))
        self.process2 = SimpleMovingAverage(list(sc.medfilt(self.data.y)))

    def getMask(self):
        self.mask = getMask(self.process1.newx)
        
    def getSets(self):
        vvector = getSets(self.process1.newx,self.mask)
#        print vvector
        self.volt = map(mean,vvector)
#        print volt
        cvector = getSets(self.process2.newx,self.mask)
#        print cvector
        self.voltcurrent = map(mean,cvector)
        #para 98,109,120,131,144
        self.offset = mean(self.voltcurrent[:5])
        self.current = np.asarray(self.voltcurrent) - self.offset*np.ones(len(self.voltcurrent))
#        print current
    
    def changeAtPoint(self,sel,data):
        self.volt[sel]=data[0]
        self.voltcurrent[sel]=data[1]
        self.current = np.asarray(self.voltcurrent) - self.offset*np.ones(len(self.voltcurrent))
        
    def getRanges(self,value):
        
        x = range(len(self.mask))
        x1 = None 
        x2 = None
        l = []
        for idx in x:
            if self.mask[idx]==value:
                if x1==None or x2 == None:
                    continue
                else:
                    l = l+[[x1,x2]]
                    x1=None
                    x2=None
            else:
                if x1==None:
                    x1=x[idx]
                else:
                    x2=x[idx]
        
        return l
    ##To test in standalone***************************************
    def plotResult(self):
#        plt.figure()
        plt.plot(tomVolts(self.volt),touAmpere(self.current),'o')

def getLimits(ldp):
    xmax = []
    xmin = []
    ymax = []
    ymin = []
    for process in ldp:
        xmax = xmax +[np.max(tomVolts(process.volt))]
        xmin = xmin + [np.min(tomVolts(process.volt))]
        ymax = ymax + [np.max (touAmpere(process.current))]
        ymin = ymin + [np.min(touAmpere(process.current))]
    
    thexmax = np.max(xmax)
    thexmin = np.min(xmin)
    theymax = np.max(ymax)
    theymin = np.min(ymin)
    
    return thexmin, thexmax, theymin, theymax
        
    
if __name__ == "__main__":
    

    dps = DataProcessor('prueba750mV.txt')
    dps.plotResult()

    dps = DataProcessor('prueba750mV-v2.txt')
    dps.plotResult()

    dps = DataProcessor('prueba750mV-v3.txt')
    dps.plotResult()
    
    dps = DataProcessor('prueba750mV-v4.txt')
    dps.plotResult()
    
    plt.figure()
    
    dps = DataProcessor('prueba800mV-v1.txt')
    dps.plotResult()
    
    dps = DataProcessor('prueba800mV-v2.txt')
    dps.plotResult()
    
    dps = DataProcessor('prueba800mV-v3.txt')
    dps.plotResult()
    
    dps = DataProcessor('prueba800mV-v4.txt')
    dps.plotResult()
## Previous implementation
#    data = dataacquire.DataAcquisition()
#    
#    data.setFile("prueba750mV-v3.txt")
#    
#    data.getData()
#    
#    plt.plot(data.x)
#    plt.plot(sc.medfilt(data.y))
#    
#    process1 = SimpleMovingAverage(list(sc.medfilt(data.x)))
#    process2 = SimpleMovingAverage(list(sc.medfilt(data.y)))
#    
#    plt.figure()
#    plt.plot(process1.newx)
#    plt.plot(process2.newx)
#    
#    mask = getMask(process1.newx)
#    plt.figure()
#    plt.plot(mask)
#    
#    vvector = getSets(process1.newx,mask)
#    print vvector
#    
#    volt = map(mean,vvector)
#    print volt
#    
#    cvector = getSets(process2.newx,mask)
#    print cvector
#    
#    current = np.asarray(volt) - np.asarray(map(mean,cvector))
#    print current
#    
#    plt.figure()
#    plt.plot(tomVolts(volt),touAmpere(current),'*')
    ##To plot data
    #http://stackoverflow.com/questions/21583965/matplotlib-cursor-value-with-two-axes