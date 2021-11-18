# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 09:45:24 2016

@author: luighi

==================================
Cursors in MatPlotLib
=================================

Based on:
    * http://stackoverflow.com/a/4674445 Joe Kington
    * http://stackoverflow.com/a/21585524 unutbu

"""
import numpy as np
from matplotlib import cbook
from scipy import spatial

import logging

##Setting the main config for logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(module)s: %(message)s',
                    )

class DataCursor(object):
    
    def __init__(self,artists, tolerance = 2, offsets= (-20,20),
                 template = 'x: %0.2f\ny: %0.2f',display_all=False):
        """Create the data cursor and connect it to the relevant figure.
        "artists" is the matplotlib artist or sequence of artists that will be 
            selected. 
        "tolerance" is the radius (in points) that the mouse click must be
            within to select the artist.
        "offsets" is a tuple of (x,y) offsets in points from the selected
            point to the displayed annotation box
        "template" is the format string to be used. Note: For compatibility
            with older versions of python, this uses the old-style (%) 
            formatting specification.
        "display_all" controls whether more than one annotation box will
            be shown if there are multiple axes.  Only one will be shown
            per-axis, regardless. 
        """
        self.template = template
        self.offsets = offsets
        self.display_all= display_all
        
        if not cbook.iterable(artists):
            artists = [artists]
            
        self.artists = artists
        self.axes = tuple(set(art.axes for art in self.artists))
        self.figures = tuple(set(art.figure for art in self.artists))
        
        self.annotations = {}
        
        for ax in self.axes:
            self.annotations[ax] = self.annotate(ax)
        
        for artist in self.artists:
            artist.set_picker(tolerance)
        
        for figure in self.figures:
            figure.canvas.mpl_connect('pick_event',self)
        
    def annotate(self,ax):
        """draws and hides the annotation in the box to a given axis"""
        annotation = ax.annotate(self.template,xy=(0,0),ha='right',
                                xytext = self.offsets, textcoords='offset points',
                                va = 'bottom',
                                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5),
                                arrowprops = dict(arrowstyle='->',
                                                  connectionstyle = 'arc3,rad=0')
                                )
        annotation.set_visible(False)
        return annotation
    
    def __call__(self,event):
        """Intended to be called through "mpl_connect" """
        x,y = event.mouseevent.xdata, event.mouseevent.ydata
        annotation = self.annotations[event.artist.axes]
        
        if x is not None:
            if not self.display_all:
                ##Hide other annotations
                for ann in self.annotations.values():
                    ann.set_visible(False)
            
            annotation.xy = x, y
            annotation.set_text(self.template % (x,y))
            annotation.set_visible(True)
            event.canvas.draw()

def fmt(x,y):
    return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x=x,y=y)
    
class FollowDotCursor(object):
    
    def __init__(self,ax,x,y,formatter = fmt,offsets = (-20,20)):
        
        try:
            x = np.asarray(x,dtype='float')
        except:
            logging.debug("Incorrect data provided")
        
        y = np.asarray(y,dtype='float')
        
        ##Detecting NaN values
        mask = ~ (np.isnan(x) | np.isnan(y))
        ##Only selects which are not nan
        x = x[mask]
        y = y[mask]
        
        ##Save new values in points
        self.__points = np.column_stack((x,y))
        
        ##Determine the scale
        #y = y[]
        
        self.tree = spatial.cKDTree(self.__points)
        self.formatter = formatter
        self.ax = ax
        self.figure = ax.figure
        self.offsets=offsets
        self.ax.xaxis.set_label_position('top')
        self.dot = ax.scatter([x.min()],[y.min()],s = 130,color= 'green', alpha = 0.7)
        self.annotation = self.setup_annotation()
        self.dot.set_visible(False)
        plt.connect('motion_notify_event',self)
        
    def __call__(self,event):
        
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            
        elif event.inaxes is None:
            return
#        else:
#            inv = ax.Trasn
        
        annotation = self.annotation
        x ,y = self.snap(x,y)
        annotation.xy = x,y
        annotation.set_text(self.formatter(x,y))
        
        annotation.set_visible(True)
        self.dot.set_offsets((x,y))
        self.dot.set_visible(True)
        event.canvas.draw()
    
    def setup_annotation(self):
        
        annotation = self.ax.annotate(
                '',xy=(0,0),ha = 'right',
                xytext = self.offsets,textcoords = 'offset points', va = 'bottom',
                bbox = dict(
                    boxstyle='round,pad=0.5', fc = 'yellow', alpha = 0.5),
                arrowprops = dict(
                    arrowstyle= '->', connectionstyle='arc3,rad=0')
                )
        annotation.set_visible(False)
        return annotation
    
    def snap(self,x,y):
        dist, idx = self.tree.query((x,y),k=1,p=1)
        try:
            return self.__points[idx]
        except IndexError:
            
            logging.debug('Index error')
            return None
            
if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    
    plt.figure()
    
    plt.subplot(1,1,1)
    ## line, copy the first object in plt.plot
    line1, = plt.plot(range(10),'ro-')
    
#    DataCursor([line1])
    
    FollowDotCursor(line1.axes,range(10),range(10))
    
    plt.show()
        
        
        