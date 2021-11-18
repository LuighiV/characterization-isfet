# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:37:49 2016

@author: lviton
"""
import sys
from PyQt4 import QtGui
from matplotlib.patches import FancyArrowPatch
import processdata as pd
import graphicplot as gp

class EditorPlot(gp.GraphicPlot):
    
    def __init__(self,processor,selected):
        super(EditorPlot,self).__init__()
        
        self.processor = processor
        self.selected = selected
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()
        
        ranges = processor.getRanges(True)
        therange = ranges[self.selected]
        self.min = therange[0]
        self.max = therange[1]
        
    def plotRaw(self):
        data= self.processor.data
        self.lin1, = self.ax.plot(data.x[self.min:self.max])
        self.lin2, = self.ax.plot(data.y[self.min:self.max])
    
    def showRaw(self):
        self.lin1.set_visible(True)
        self.lin2.set_visible(True)
    
    def hideRaw(self):
        self.lin1.set_visible(False)
        self.lin2.set_visible(False)
    
    def plotFiltered(self):
        p1 = self.processor.process1
        p2 = self.processor.process2
        
        self.new1, = self.ax.plot(p1.newx[self.min:self.max])
        self.new2, = self.ax.plot(p2.newx[self.min:self.max])
    
    def showFiltered(self):
        self.new1.set_visible(True)
        self.new2.set_visible(True)
    
    def hideFiltered(self):
        self.new1.set_visible(False)
        self.new2.set_visible(False)
        
    def plotMean(self):
        self.hline1 = self.ax.axhline(self.processor.volt[self.selected])
        self.hline2 = self.ax.axhline(self.processor.voltcurrent[self.selected])
        
        self.dragl = DragLine([self.hline1,self.hline2])
        self.diffl = DiffLine([self.hline1,self.hline2])
        
    def resetPlot(self):
        self.hline1.set_ydata([self.processor.volt[self.selected]]*2)
        self.hline2.set_ydata([self.processor.voltcurrent[self.selected]]*2)
        
        self.dragl.updateData()
        self.diffl.updateData()

class DragLine(object):
    
    def __init__(self,artists):
        
        self.artists = artists
        self.figures = tuple(set(art.figure for art in self.artists))
        
        self.annotations = {}
        
        for art in self.artists:
            art.set_picker(5)
            ax = art.axes
            y = art.get_ydata()[0]
            self.annotations[art] = self.annotate(ax,y)
        
#        print self.annotations
        
        for figure in self.figures:
            figure.canvas.mpl_connect("pick_event",self)
            figure.canvas.mpl_connect("motion_notify_event",self.on_motion)
            figure.canvas.mpl_connect("button_release_event",self.on_release)
        
        self.picked=None
        self.currentartist=None
    
    def annotate(self,ax,y):
        
        xmin, xmax, ymin, ymax = ax.axis()
        annotation = ax.annotate('x: {x:0.2f}\n V: {v:0.2f}m'.format(x=y,v=pd.tomVolts(y)),xy=(xmax,y),
                        ha='right',xytext = (-1,0), textcoords='offset points',
                        va = 'bottom',bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5))
        return annotation
        
    def __call__(self,event):
        self.currentartist= event.artist
        self.picked=True
        event.canvas.draw()
        
    def on_motion(self,event):
        y = event.ydata
        if self.currentartist is not None:
#            print  hex(id(self.currentartist))
            self.currentartist.set_ydata([y,y])
            ax = self.currentartist.axes
            xmin, xmax, ymin, ymax = ax.axis()
#            print self.annotations
            annotation = self.annotations[self.currentartist]
            annotation.xy = xmax, y
            annotation.set_text('x: {x:0.2f}\n V: {v:0.2f}m'.format(x=y,v=pd.tomVolts(y)))
        
        event.canvas.draw()
        
    def on_release(self,event):
        self.currentartist=None
        self.picked=False
        
    def disconnectEvents(self):
        for figure in self.figures:
            figure.canvas.mpl_disconnect(self)
            figure.canvas.mpl_disconnect(self.on_motion)
            figure.canvas.mpl_disconnect(self.on_release)
    
    def updateData(self):
        for art in self.artists:
            ax = art.axes
            y = art.get_ydata()[0]
            xmin, xmax, ymin, ymax = ax.axis()
            annotation = self.annotations[art]
            annotation.xy = xmax, y
            annotation.set_text('x: {x:0.2f}\n V: {v:0.2f}m'.format(x=y,v=pd.tomVolts(y)))
        
class DiffLine(object):
    
    def __init__(self,artists):
        
        self.artists = [artists[0],artists[1]]
        self.figure = self.artists[0].figure
        
        self.ax = self.artists[0].axes
        y1 = self.artists[0].get_ydata()[0]
#        print y1
        y2 = self.artists[1].get_ydata()[0]
#        print y2
        self.arrow,self.annotation = self.annotate(self.ax,y1,y2)
        
        self.figure.canvas.mpl_connect("pick_event",self)
        self.figure.canvas.mpl_connect("motion_notify_event",self.on_motion)
        self.figure.canvas.mpl_connect("button_release_event",self.on_release)
        
        self.picked=None
        self.currentartist=None
        
    def annotate(self,ax,y1,y2):
        diff = y2-y1
        xmin, xmax, ymin, ymax = ax.axis()
        ##From http://matthiaseisen.com/matplotlib/shapes/arrow/
        arrow = FancyArrowPatch(posA=(xmax*.75,y1),posB=(xmax*.75,y2),arrowstyle='<->',mutation_scale=20)
        ax.add_patch(arrow)
        annotation = ax.annotate('diff: {diff:0.2f}\n A: {a:0.2f}u'.format(diff=diff,a=pd.touAmpere(diff)),xy=(xmax*.75,y1+diff/2),
                        ha='left',xytext = (0,0), textcoords='offset points',
                        va = 'center',bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5))
        return arrow,annotation
    
    def __call__(self,event):
        self.picked=True
        self.currentartist=event.artist
        event.canvas.draw()
        
    def on_motion(self,event):
        if self.picked is not None:
            y = event.ydata
            
            if self.currentartist is self.artists[0]:
                y1 = y
                y2 = self.artists[1].get_ydata()[0]
                self.updateYData(y1,y2)
                
            elif self.currentartist is self.artists[1]:
                y1 = self.artists[0].get_ydata()[0]
                y2 = y
                self.updateYData(y1,y2)
                
        event.canvas.draw()
        
    def on_release(self,event):
        self.picked=None
        self.currentartist=None
#        self.updateData()
        event.canvas.draw()
    
    def updateData(self):
        y1 = self.artists[0].get_ydata()[0]
        y2 = self.artists[1].get_ydata()[0]
        self.updateYData(y1,y2)
        
    def updateYData(self,y1,y2):
        xmin, xmax, ymin, ymax = self.ax.axis()
        diff = y2-y1
        self.annotation.xy = xmax*0.75,y1+diff/2
        self.annotation.set_text('diff: {diff:0.2f}\n A: {a:0.2f}u'.format(diff=diff,a=pd.touAmpere(diff)))
        self.arrow.set_positions((xmax*.75,y1), (xmax*.75,y2))
        
    def disconnectEvents(self):
        self.figure.canvas.mpl_disconnect(self)
        self.figure.canvas.mpl_disconnect(self.on_motion)
        self.figure.canvas.mpl_disconnect(self.on_release)
    
    
if __name__ == "__main__":
    import processdata as pd
    
    dps = pd.DataProcessor('prueba750mV.txt')
    
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    
    ap = EditorPlot(dps,12)
    mw.setCentralWidget(ap)
    
    ap.plotRaw()
    ap.plotFiltered()
    ap.plotMean()
    
    mw.show()
    
    sys.exit(app.exec_())
