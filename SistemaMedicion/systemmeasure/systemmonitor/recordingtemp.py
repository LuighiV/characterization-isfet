# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:07:26 2016

@author: lviton
"""

import sys
sys.path.append("../")
import recording as rec
import logging


##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )
                    

class RecordingWidget(rec.RecordingWidget):
    """
    Class to provide the object of serial Module
    """
    def __init__(self,parent=None):
        super(RecordingWidget,self).__init__()
        
    def recordTempData(self,temp,tempntc,volt,ph):
        self.f.write(', '.join([str(temp),str(tempntc),str(volt),str(ph)]) + '\n')