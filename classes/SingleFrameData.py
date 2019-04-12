"""
===============================================================================
                      Python code for PIV analysis
   Created by Combustion Research Center CRC at LETE - Sao Paulo, Brasil
   Laboratory of Environmental and Thermal Engineering - LETE
   Escola Politecnica da USP - EPUSP
   
===============================================================================
version:0.0 - 02/2019: Helio Villanueva
version:1.0 - 04/2019: Helio Villanueva
"""

import re
import numpy as np


class SingleFrameData(object):
    '''
    Class to read data at each timestep
    
    Methods are: readFrame(time), readFrameCoordinates(time),
    readFrameVelocities(time), printCoordInfos().
    '''
    def __init__(self,fRes):
        self.fRes = fRes
        self.fRes.sort()
        with open(fRes[0]) as f:
            content = f.readlines()
            size = re.findall(r'I=(.*) J=(.*) ',content[2])
            self.cols = int(size[0][0])
            self.lins = int(size[0][1])
            
        self.xcoord,self.ycoord = self.readFrameCoordinates(0)
        self.xscale = (self.xcoord.max() - self.xcoord.min())*0.001/self.cols
        self.yscale = (self.ycoord.max() - self.ycoord.min())*0.001/self.lins
        self.xmin = self.xcoord.min()
        self.xmax = self.xcoord.max()
        self.ymin = self.xcoord.min()
        self.ymax = self.ycoord.max()
        self.Lx = np.abs(self.xmin) + self.xmax
        self.Ly = np.abs(self.ymin) + self.ymax
        
    def readFrame(self,time):
        '''Method to read the coordinates and velocity fields for one 
        "time"step.
        Returns x,y,U,V arrays
        '''
        xt,yt = self.readFrameCoordinates(time)
        Ut,Vt = self.readFrameVelocities(time)
        
        return xt,yt,Ut,Vt
    
    def _readFrame_(self,time,usecols):
        '''Function to read each frame for coordinates or velocities
        '''
        data_dantec = np.genfromtxt(self.fRes[time],skip_header=3,skip_footer=6,usecols=usecols)
        
        fxt = np.flipud(data_dantec[:,0].reshape((self.lins,self.cols)))
        fyt = np.flipud(data_dantec[:,1].reshape((self.lins,self.cols)))
        
        return fxt,fyt
        
    def readFrameCoordinates(self,time):
        usecols = (4,5)
        
        xt, yt = self._readFrame_(time,usecols)
        
        return xt,yt

    def readFrameVelocities(self,time):
        '''readFrameVelocities method
        '''
        usecols = (8,9)
        
        Ut, Vt = self._readFrame_(time,usecols)
        
        return Ut,Vt
    
    def printCoordInfos(self):        
        print('===============')
        print('Bounding Box\n===============')
        print('X coordinates: (' + str(self.xmin) + ', ' + str(self.xmax) + ') Lx: ' + str(self.Lx))
        print('X Scale: ' + str(self.xscale) + ' m/pixel\n')
        print('Y coordinates: (' + str(self.ymin) + ', ' + str(self.ymax) + ') Ly: ' + str(self.Ly))
        print('Y Scale: ' + str(self.yscale) + ' m/pixel')
        
        return 0