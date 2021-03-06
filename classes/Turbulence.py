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
from scipy import signal


class Turb(ReadData):
    '''class containing turbulence/statistics methods/data
    
    u, v -> instantaneous velocity data
    
    U, V -> time average velocities
    
    uL, vL -> velocity fluctuations (as function to use less ram)
    
    uu, vv, uv -> Reynolds Stress components
    '''
    def __init__(self,resPath,u,v):
        print('Initializing turbulence calculations')
        ReadData.__init__(self,resPath)
        self.u = u
        self.v = v
        self.U = np.mean(self.u,axis=2, keepdims=True)
        self.V = np.mean(self.v,axis=2, keepdims=True)
        self.magVel = np.sqrt(self.U**2 + self.V**2)
        self.varU = np.mean(self.uL()**2,axis=2, keepdims=True)
        self.varV = np.mean(self.vL()**2,axis=2, keepdims=True)
        self.stdDevU = np.sqrt(self.varU)
        self.stdDevV = np.sqrt(self.varV)
        
        self.calcReStress()
        self.calcVelGrad()
        print('Done')

        
    def uL(self):
        return self.u - self.U
    
    def vL(self):
        return self.v - self.V
    
    def calcReStress(self):
        self.uu = np.mean(self.uL()*self.uL(),axis=2, keepdims=True)
        self.vv = np.mean(self.vL()*self.vL(),axis=2, keepdims=True)
        self.uv = np.abs(np.mean(self.uL()*self.vL(),axis=2, keepdims=True))
        return 0
    
    def calcK2DPIV(self):
        '''calculates the turbulent kinetic energy for 2D PIV by assuming the
        flow to be locally isotropic
        '''
        K = 3./4 *(self.uu + self.vv)
        return K
    
    def calcKPIV(self):
        '''calculates the turbulent kinetic energy for 2D3C PIV.
        ****not implemented****
        '''
        return 0
    
    def calcVelGrad(self):
        '''calculates the velocity gradient tensor
        '''
        # - Fourth order CDS scheme from Ferziger Computational methods for
        # - fluid dynamics on page 44 eq 3.14
        scheme = np.array([[0,0,0,0,0],[1,-8,0,8,-1],[0,0,0,0,0]])

        U = self.U[:,:,0]
        V = self.V[:,:,0]
        # - gradients on x direction
        numUx = signal.convolve(U,scheme, mode='same')
        numVx = signal.convolve(V,scheme, mode='same')
        # dU/dx
        self.grad11 = numUx/(12*self.xscale)
        # dV/dx
        self.grad21 = numVx/(12*self.xscale)
        
        # - gradients on y direction
        numUy = signal.convolve(U,scheme.transpose(), mode='same')
        numVy = signal.convolve(V,scheme.transpose(), mode='same')
        # dU/dy
        self.grad12 = numUy/(12*self.yscale)
        # dV/dy
        self.grad22 = numVy/(12*self.yscale)
        return 0
    
    def calcSij(self):
        '''calculate Sij tensor for 2D2C - S11, S22, S12
        '''
        S11 = self.grad11
        S22 = self.grad22
        S12 = 0.5*(self.grad21 + self.grad12)

        SijSij = 2*(self.grad11)**2. + 2*(self.grad22)**2.
        SijSij += 2*(self.grad11*self.grad22) 
        SijSij += 3./2*(self.grad12 + self.grad21)**2
        
        magSij = np.sqrt(SijSij)
        return S11, S22, S12, magSij
    
    def calcTauijSmagorinsky(self):
        '''calculate the modeled tauij tensor - SGS tensor based on smagorinsky
        method
        
        Smagorinsky (1963)
        '''
        S11, S22, S12, magSij = self.calcSij()
        Cs = 0.17 # Lilly 1967 | Cheng 1997 Cs = 0.12
        delta = self.xscale # window size which the vel field is spatially avg
        const = -(Cs**2.)*(delta**2.)*magSij
        tau11 = const*S11
        tau22 = const*S22
        tau12 = const*S12
        return tau11, tau22, tau12
    
    def calcTauijGradient(self):
        '''calculate the modeled tauij tensor - SGS tensor based on gradient
        method
        
        Clark et al. (1979)
        '''
        delta = self.xscale
        const = (delta**2.)/12.
        tau11 = const*(self.grad11**2. + self.grad12**2.)
        tau22 = const*(self.grad21**2. + self.grad22**2.)
        tau12 = const*(self.grad21*self.grad11 + self.grad22*self.grad12)
        return tau11, tau22, tau12
    
    def calcEpsilon(self, method='smagorinsky'):
        '''calcluate the dissipation rate using smagorinsky or gradient methods
        '''
        S11, S22, S12, magSij = self.calcSij()
        
        if method=='gradient':
            print('gradient method')
            tau11, tau22, tau12 = self.calcTauijGradient()
        else:
            print('smagorisky method')
            tau11, tau22, tau12 = self.calcTauijSmagorinsky()
            
        epsilon = tau11*S11 + tau11*S12 + tau12*S22
        epsilon += tau12*S11 + tau22*S12 + tau22*S22
        epsilon += 2*tau12*S12
        epsilon = -200.*epsilon
        return epsilon
    
    # Calc uncertainties Mean Vel, Reynolds Stress components