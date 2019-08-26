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
from glob import glob

class SingleFrameData(object):
    '''
    Class to read data at each timestep
    
    Methods are: readFrame(time), readFrameCoordinates(time),
    readFrameVelocities(time), printCoordInfos().
    '''
    def __init__(self,resPath):
        self.resPath = resPath
        print('Reading files from: ' + str(self.resPath))
        self.files = glob(resPath + '/*.dat')
        self.files.sort()
        with open(self.files[0]) as f:
            content = f.readlines()
            # - get size of data as n pixels (lins,cols)
            size = re.findall(r'I=(.*) J=(.*) ',content[2])
            self.cols = int(size[0][0])
            self.lins = int(size[0][1])
            # - get variables available from file
            self.variables = content[1].split('" "')
            # - get single frame x and y coordinates
            self.xcoord,self.ycoord = self.readFrameCoordinates(0)
            
        self.calcCoordProps()
        
    def readFrameCoordinates(self,time):
        self.xcoordidx = self.variables.index("x (mm)[mm]")
        self.ycoordidx = self.variables.index("y (mm)[mm]")
        
        usecols = (self.xcoordidx,self.ycoordidx)
        
        xt,yt = self._readFrame_(time,usecols)
        
        return xt, yt
    
    def _readFrame_(self,time,usecols):
        '''Function to read each frame for coordinates or velocities
        '''
        data_dantec = np.genfromtxt(self.files[time],skip_header=3,skip_footer=6,usecols=usecols)
        
        fxt = np.nan_to_num(np.flipud(data_dantec[:,0].reshape((self.lins,self.cols))))
        fyt = np.nan_to_num(np.flipud(data_dantec[:,1].reshape((self.lins,self.cols))))
        
        return fxt,fyt
         
    def readFrame1Variable(self,time,varXname):
        '''readFrame1Variable method
        Reads a specified variable from the .dat file for a specific timestep
        ex: varXname = "Rms U[pix]"
        '''
        varxidx = self.variables.index(varXname)
        
        usecols = (varxidx)
        
        varXt, varYt = self._readFrame_(time,usecols)
        
        return varXt
    
    def readFrameVariable(self,time,varXname,varYname):
        '''readFrameVariable method
        Reads two specified variable from the .dat file for a specific timestep
        ex: varXname = "Rms U[pix]"
        '''
        varxidx = self.variables.index(varXname)
        varyidx = self.variables.index(varYname)
        
        usecols = (varxidx,varyidx)
        
        varXt, varYt = self._readFrame_(time,usecols)
        
        return varXt,varYt
    
    def calcCoordProps(self):
        '''Function to calculate properties of the coordinates as object props
        '''
        self.xscale = (self.xcoord.max() - self.xcoord.min())*0.001/self.cols
        self.yscale = (self.ycoord.max() - self.ycoord.min())*0.001/self.lins
        self.xmin = self.xcoord.min()
        self.xmax = self.xcoord.max()
        self.ymin = self.xcoord.min()
        self.ymax = self.ycoord.max()
        self.Lx = np.abs(self.xmin) + self.xmax
        self.Ly = np.abs(self.ymin) + self.ymax
        return 0
    
    def printCoordInfos(self):        
        #print('-------------')
        print('Bounding Box\n-------------')
        print('X x Y: ' + str(self.cols) + ' x ' + str(self.lins) + ' vectors')
        print('X coordinates: (' + str(self.xmin) + ', ' + str(self.xmax) + ') Lx: ' + str(self.Lx))
        print('X Scale: ' + str(self.xscale) + ' m/pixel\n')
        print('Y coordinates: (' + str(self.ymin) + ', ' + str(self.ymax) + ') Ly: ' + str(self.Ly))
        print('Y Scale: ' + str(self.yscale) + ' m/pixel')
        
        return 0
    
    def calcPIVres(self, LIC, LCCD):
        '''Function to calculate PIV resolution and the smallest scale
        Lr -> smallest length scale available
        LIC -> dimension of the interrogation cell (eg 32 pixels)
        LCCD -> dimension of the CCD array (eg 1028 pixels)
        Lv -> length scale of the viewing area
        '''
        Lv = np.mean(self.Lx, self.Ly)
        Lr = (LIC/LCCD)*Lv
        return Lr


## OLD NOT USED
#    def readFrame(self,time):
#        '''Method to read the coordinates and velocity fields for one 
#        "time"step.
#        Returns x,y,U,V arrays
#        '''
#        Uxidx = self.variables.index("U[m/s]")
#        Uyidx = self.variables.index("V[m/s]")
#        usecolsXY = (self.xcoordidx,self.ycoordidx)
#        usecolsUV = (Uxidx,Uyidx)
#        
#        xt,yt = self._readFrame_(time,usecolsXY)
#        Ut,Vt = self._readFrame_(time,usecolsUV)
#        
#        return xt,yt,Ut,Vt