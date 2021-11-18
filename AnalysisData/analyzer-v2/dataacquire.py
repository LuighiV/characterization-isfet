# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 17:57:40 2016

@author: lviton
"""

import numpy as np
import matplotlib.pyplot as plt

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )

class DataAcquisition :
    
    def __init__(self):
        
        self.f = None
        self.x = []
        self.y = []
        
    def setFile(self,filename):
        self.f = open(filename,'r')
        
    def getData(self):
        
        for line in self.f:
            numbers = line.split(',')
            ##Changed in new version regarding changes in position of ADCs
            self.x.append(int(numbers[1]))
            self.y.append(int(numbers[0]))

if __name__ == "__main__":
    
    data = DataAcquisition()
    
    data.setFile("prueba1.txt")
    
    data.getData()
    
    logging.debug("Data x" + '\n'.join(map(str,data.x)))
    logging.debug("Data y" + '\n'.join(map(str,data.y)))
    
    plt.plot(data.x)
    plt.plot(data.y)