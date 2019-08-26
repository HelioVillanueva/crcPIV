"""
===============================================================================
                      Python code for PIV analysis
   Created by Combustion Research Center CRC at LETE - Sao Paulo, Brasil
   Laboratory of Environmental and Thermal Engineering - LETE
   Escola Politecnica da USP - EPUSP
   
===============================================================================
version:0.0 - 02/2019: Helio Villanueva
version:1.0 - 04/2019: Helio Villanueva
version:1.1 - 08/2019: Helio Villanueva
"""

import matplotlib.pyplot as plt
import numpy as np

        
class baseSeeding(object):
    '''Abstract class for Seeding calculations
    rho -> particle\n
    dp -> mean particle diameter\n
    mu -> fluid dynamic viscosity\n
    '''
    def __init__(self):
        self.rho = 1
        self.dp = 1
        self.mu = 1
        self.C = 1
        
    def graphResponse(self,ymin=0.1):
        '''func/method to plot response vs max frequency measured
        '''
        #ymin = 0.8
        resp = np.arange(ymin,1.0,0.001)
        
        fc = self.C/(2*np.pi) * (1./resp - 1)
        
        plt.figure(figsize=(8,6),dpi=150)
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.plot(fc, resp,'k')
        #plt.plot(foil, resp, 'b')
        plt.xscale('log')
        plt.ylim(ymin,1.0)
        plt.hlines(0.95,min(fc),1.2e4,linestyles='dashed')
        plt.vlines(1.2e4, 0,0.95, linestyles='dashed')
        #plt.grid(which='minor')
        #plt.grid(which='major')
        plt.xlabel(r'\textbf{$f_c$} (Hz)', fontsize=16)
        plt.ylabel(r"$\frac{\overline{u_p^2}}{\overline{u_f^2}}\;$", rotation=0,fontsize=20,labelpad=15)
        plt.xticks(fontsize=16)
        plt.yticks((0.8,0.85,0.9,0.95,1),(r'0.8',r'0.85',r'0.9',r'0.95',r'1'),fontsize=16)
        plt.annotate(r'$C=\frac{18\mu}{\rho_p d_p^2}$',(3.5e5,0.4),(1e6,0.5),arrowprops=dict(arrowstyle='->'), fontsize=18)
        #plt.annotate(r'0.95',(1e6,0.95),(2e6,0.8),arrowprops=dict(arrowstyle='->'),fontsize=15)
        plt.show()
        
class SiO2(baseSeeding):
    '''Class for solid seeding of SiO2
    rho -> particle\n
    dp -> mean particle diameter\n
    mu -> fluid dynamic viscosity\n
    '''
    def __init__(self,mu=1.837e-6):
        baseSeeding.__init__(self)
        self.rho = 260.
        self.dp = 0.3e-6
        self.mu = mu
        self.C = 18*self.mu/(self.rho*(self.dp**2))
        
class Sebacate(baseSeeding):
    '''Class for liquid seeding of Sebacate Oil
    rho -> particle\n
    dp -> mean particle diameter\n
    mu -> fluid dynamic viscosity\n
    '''
    def __init__(self,mu=1.837e-6):
        baseSeeding.__init__(self)
        self.rho = 916.
        self.dp = 3e-6
        self.mu = mu
        self.C = 18*self.mu/(self.rho*(self.dp**2))
        

## OLD NOT USED
#class Seeding(object):
#    '''class for seeding properties calculations and uncertainties
#    '''
#    def __init__(self):
#        # Seeding solido SiO2
#        self.SiO2 = Tracer(260., 0.3e-6, 1.837e-6)
#
#        # Seeding liquido
#        self.Oil = Tracer(916., 1e-6, 1.837e-6)
#        
#    def graphResponse(self):
#        '''func/method to plot response vs max frequency measured
#        '''
#        ymin = 0.8
#        resp = np.arange(ymin,1.0,0.001)
#        
#        fc = self.SiO2.C/(2*np.pi) * (1./resp - 1)
#        #foil = self.Oil.C/(2*np.pi) * (1./resp - 1)
#        
#        plt.figure(figsize=(8,6),dpi=150)
#        plt.rc('text', usetex=True)
#        plt.rc('font', family='serif')
#        plt.plot(fc, resp,'k')
#        #plt.plot(foil, resp, 'b')
#        plt.xscale('log')
#        plt.ylim(ymin,1.0)
#        plt.hlines(0.95,min(fc),1.2e4,linestyles='dashed')
#        plt.vlines(1.2e4, 0,0.95, linestyles='dashed')
#        #plt.grid(which='minor')
#        #plt.grid(which='major')
#        plt.xlabel(r'\textbf{$f_c$} (Hz)', fontsize=16)
#        plt.ylabel(r"$\frac{\overline{u_p^2}}{\overline{u_f^2}}\;$", rotation=0,fontsize=20,labelpad=15)
#        plt.xticks(fontsize=16)
#        plt.yticks((0.8,0.85,0.9,0.95,1),(r'0.8',r'0.85',r'0.9',r'0.95',r'1'),fontsize=16)
#        plt.annotate(r'$C=\frac{18\mu}{\rho_p d_p^2}$',(3.5e5,0.4),(1e6,0.5),arrowprops=dict(arrowstyle='->'), fontsize=18)
#        #plt.annotate(r'0.95',(1e6,0.95),(2e6,0.8),arrowprops=dict(arrowstyle='->'),fontsize=15)
#        plt.show()
#        
#        return 0
#    
#class Tracer(object):
#    '''abstract class for tracer particle or droplet\n
#    rho -> particle\n
#    dp -> mean particle diameter\n
#    mu -> fluid dynamic viscosity\n
#    '''
#    def __init__(self,rho,dp,mu=1.837e-6):
#        self.rho = rho # kg/m3
#        self.dp = dp # m
#        self.mu = mu
#        self.C = 18*self.mu/(self.rho*(self.dp**2))