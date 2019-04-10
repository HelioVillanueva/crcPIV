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

from classes.SingleFrameData import SingleFrameData, np
from progressbar import ProgressBar

class ReadData(SingleFrameData):
    '''
    Class to read all timesteps from Dantec Data
    fRes list of raw PIV files from Dantec
    '''
    def __init__(self,fRes):
        SingleFrameData.__init__(self,fRes)
        self.Ttot = len(self.fRes)
        
    def read(self,resPath):
        '''Method to read the raw data if there is no U.py ou V.py file
        Return U,V
        '''
        try:
            U = np.load(resPath + '/U.npy')
            print('Reading PIV data in python format\n')
            V = np.load(resPath + '/V.npy')
            Uf,Vf = self.readFrameVelocities(0)
            
        except:
            print('Reading PIV raw files')
        
            Uf,Vf = self.readFrameVelocities(0)
            U,V = self.readVelTimeSeries()
            
            print('Saving PIV data in python format')
            np.save(resPath + '/U',U)
            np.save(resPath + '/V',V)
            
        return U,V
        
    def readVelTimeSeries(self):
        
        print('Generating velocities matrices')
        U = np.zeros((self.lins, self.cols, self.Ttot))
        V = np.zeros((self.lins, self.cols, self.Ttot))
        
        print('Reading PIV Frames - Velocity components')
        pbar = ProgressBar()
        pbar.start()
        
        ## -- Loop over all files/times
        for time,name in enumerate(self.fRes):
            
            if time==0:
                perc = 0.
            else:
                perc = time/float(self.Ttot)*100.
            
            U[:,:,time],V[:,:,time] = self.readFrameVelocities(time)
            
            pbar.update(perc)
        
        pbar.finish()
        
        return U,V