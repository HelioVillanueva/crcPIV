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

from classes.ReadData import ReadData
import matplotlib.pyplot as plt
import numpy as np

class Plots(ReadData):
    '''Class for ploting results
    '''
    def __init__(self,resPath):
        ReadData.__init__(self,resPath)
        self.extent = [self.xmin,self.xmax,self.ymin,self.ymax]
        self.xlabel = 'Radius [mm]'
        self.ylabel = r'y [mm]'
        self.interpolation = 'bicubic'
        
        
    def singleFramePlot(self,data,dataName,t=0,grid='off'):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.figure(figsize=(5.5,6),dpi=150)
        ax = plt.gca()
        im = ax.imshow(data[:,:,t],cmap='jet',interpolation=self.interpolation,
                       extent=self.extent)
        ax.set_title('Time: %8.3f s' %self.timeStamp[t], fontsize=16)
        plt.xlabel(self.xlabel, fontsize=16)
        plt.ylabel(self.ylabel, fontsize=16)
        ax.set_xticks(np.arange(self.xmin,self.xmax), minor=True)
        ax.set_yticks(np.arange(self.ymin,self.ymax), minor=True)
        ax.tick_params(which='minor', bottom=False, left=False)
        plt.xticks(size=16)
        plt.yticks(size=16)
        if grid!='off':
            plt.grid(which='minor',color='k') 
        cbar = ax.figure.colorbar(im)
        cbar.ax.tick_params(labelsize=16)
        cbar.set_label(dataName,size=16) #,rotation=0,y=1.05,labelpad=-17
        
        
    def plothLine(self,data,y,name,err=np.array([0]),CFD=0,xcorr=0):
        '''method to plot horizontal lines
        CFD = [CFD_x*-1000,CFD_velMag]
        '''
        dl = self.gethline(data,y)
        
        if err.any()!=0:
            yerr = self.gethline(err[:,:,0],y)
        else:
            yerr = 0
        
        plt.figure(figsize=(6,6),dpi=150)
        if CFD!=0:
            plt.plot(CFD[0],CFD[1],'k',label='CFD')
        plt.errorbar(self.xcoord[0,:]+xcorr,dl,yerr=yerr,fmt='o',ecolor='k',c='k',
                     ms=3,capsize=2,lw=1,label='PIV')
        plt.legend()
        plt.xlabel('Radius [mm]', size=16)
        plt.ylabel(name, size=16)
        plt.xticks(size=16)
        plt.yticks(size=16)
        plt.title('$Y = 0.13 [m]$', size=18)
        return 0
    
    def gethline(self,data,y):
        '''friend function to interpolate horizontal line values from y\n
        y unit same as dantec saved\n
        hline -> linear interpolated horizontal line using 2 closest values of y
        '''
        idxd, idxu, yd, yu = self.gety_idx(y)
        
        M = (y-yd)/(yu-yd)
        
        hline = data[idxd,:] + M*(data[idxu,:] - data[idxd,:])
        
        return hline
    
    def getvline(self,data,x):
        '''friend function to interpolate vertical line values from x\n
        x unit same as dantec saved
        vline -> linear interpolated vertical line using 2 closest values of x
        '''
        idxd, idxu, xd, xu = self.getx_idx(x)
        
        M = (x-xd)/(xu-xd)
        
        vline = data[:,idxd] + M*(data[:,idxu] - data[:,idxd])

        return vline
    
    def gety_idx(self,value):
        '''friend method to get closest indexes from y value (horizontal line)
        also return y values for interpolation
        '''
        d = np.abs(self.ycoord[:,0] - value)
        idxd = np.argsort(d)[0]
        idxu = np.argsort(d)[1]
        yd = self.ycoord[idxd,0]
        yu = self.ycoord[idxu,0]
        
        return idxd, idxu, yd, yu
    
    def getx_idx(self,value):
        '''friend method to get closest indexes from x value (vertical line)
        also return x values for interpolation
        '''
        d = np.abs(self.xcoord[0,:] - value)
        idxd = np.argsort(d)[0]
        idxu = np.argsort(d)[1]
        xd = self.xcoord[0,idxd]
        xu = self.xcoord[0,idxu]
        
        return idxd, idxu, xd, xu