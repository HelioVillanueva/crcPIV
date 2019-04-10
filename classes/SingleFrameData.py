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
        
    def readFrame(self,time):
        '''Method to read the coordinates and velocity fields for one 
        "time"step.
        Returns x,y,U,V arrays
        '''
        xt,yt = self.readFrameCoordinates(time)
        Ut,Vt = self.readFrameVelocities(time)
        
        return xt,yt,Ut,Vt
        
    def readFrameCoordinates(self,time):
        
        data_dantec = np.genfromtxt(self.fRes[time],skip_header=3,skip_footer=6,usecols=(4,5))
        
        xt = np.flipud(data_dantec[:,0].reshape((self.lins,self.cols)))
        yt = np.flipud(data_dantec[:,1].reshape((self.lins,self.cols)))
        # calc max/min on x and y coordinates
        
        
        return xt,yt

    def readFrameVelocities(self,time):
        '''readFrameVelocities method
        '''
        data_dantec = np.genfromtxt(self.fRes[time],skip_header=3,skip_footer=6,usecols=(8,9))
        
        Ut = np.flipud(data_dantec[:,0].reshape((self.lins,self.cols)))
        Vt = np.flipud(data_dantec[:,1].reshape((self.lins,self.cols)))
        
        return Ut,Vt
    
    def printCoordInfos(self):
        xcoord,ycoord = self.readFrameCoordinates(0)
        xscale = (xcoord.max()-xcoord.min())/self.cols
        yscale = (ycoord.max()-ycoord.min())/self.lins
        xmin = xcoord.min()
        xmax = xcoord.max()
        ymin = xcoord.min()
        ymax = ycoord.max()
        dx = np.abs(xmin) + xmax
        dy = np.abs(ymin) + ymax
        
        print('===============')
        print('Bounding Box\n===============')
        print('X coordinates: (' + str(xmin) + ', ' + str(xmax) + ') dx: ' + str(dx))
        print('X Scale: ' + str(xscale) + ' mm/pixel\n')
        print('Y coordinates: (' + str(ymin) + ', ' + str(ymax) + ') dy: ' + str(dy))
        print('Y Scale: ' +str(yscale) + ' mm/pixel\n')
        
        return 0