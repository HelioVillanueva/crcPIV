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

from classes.ReadData import ReadData
import numpy as np

class Turb(ReadData):
    '''class containing turbulence/statistics methods/data
    
    u, v -> instantaneous velocity data
    
    U, V -> time average velocities
    
    uL, vL -> velocity fluctuations (as function to use less ram)
    
    uu, vv, uv -> Reynolds Stress components
    '''
    def __init__(self,fRes,u,v):
        ReadData.__init__(self,fRes)
        self.u = u
        self.v = v
        self.U = np.mean(self.u,axis=2, keepdims=True)
        self.V = np.mean(self.v,axis=2, keepdims=True)
        
        self.calcReStress()
        
        
    def uL(self):
        return self.u - self.U
    
    def vL(self):
        return self.v - self.V
    
    def calcReStress(self):
        self.uu = np.mean(self.uL()*self.uL(),axis=2, keepdims=True)
        self.vv = np.mean(self.vL()*self.vL(),axis=2, keepdims=True)
        self.uv = np.abs(np.mean(self.uL()*self.vL(),axis=2, keepdims=True))
        return 0