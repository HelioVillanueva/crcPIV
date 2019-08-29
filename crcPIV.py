#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
                      Python code for PIV analysis
   Created by Combustion Research Center CRC at LETE - Sao Paulo, Brasil
   Laboratory of Environmental and Thermal Engineering - LETE
   Escola Politecnica da USP - EPUSP

===============================================================================
version:0.0 - 02/2019: Helio Villanueva
version:1.0 - 04/2019: Helio Villanueva
version:2.0 - 08/2019: Helio Villanueva
"""

import numpy as np
from classes.ReadData import ReadData
from classes.Seeding import SiO2
from classes.Turbulence import Turb
from classes.VisualPost import Plots
from classes.WriteVTK import WVTK

import matplotlib.pyplot as plt
from scipy import signal

#******************************************************************************
print('\nStart crcPIV\n')
#******************************************************************************


#******************************************************************************
## -- Read PIV Raw files
#******************************************************************************

## -- Path to the PIV velocity results files
velPath = '/home/helio/Desktop/Res0/Full/ColdSym_1khz_3s-2'

## -- Instance of class with PIV velocity results infos
velRaw = ReadData(velPath)

## -- Read PIV data. If python format already present read it instead
u,v = velRaw.read2VarTimeSeries('U[m/s]','V[m/s]')

## --

## -- Path to the PIV uncertainty results files
uncPath = '/home/helio/Desktop/Res0/Full/uncertainty'

## -- Instance of class with PIV uncertainty results infos
uncRaw = ReadData(uncPath)

## -- Read PIV data. If python format already present read it instead
uncR = uncRaw.read1UncTimeSeries('UncR(m/s)[m/s]')

## -- Print infos about coordinates and size of Field-of-View (FOV)
uncRaw.printCoordTimeInfos()

#******************************************************************************
## -- Read CFD data in csv from plotoverline paraview
#******************************************************************************
CFD = np.genfromtxt('/home/helio/Desktop/Res0/CFD/ParaView-RSM_BSL/y013.csv',
                    skip_header=1,delimiter=',')

CFD_x, CFD_velMag, CFD_epsilon = CFD[:,14], CFD[:,0], CFD[:,4]
CFD_uu, CFD_vv, CFD_uv = CFD[:,7], CFD[:,8], CFD[:,10]


#******************************************************************************
## -- Seeding tracers
#******************************************************************************

tracer = SiO2()
#tracer.graphResponse(ymin=0.8)


#******************************************************************************
## -- Turbulence calculations (velocity mean and magnitude)
#******************************************************************************

turb = Turb(velPath,u,v)


#FFTu = np.fft.rfft(turb.u[90,30,:])
#frequ = np.fft.rfftfreq(raw.Raw.Ttot,1./fa)


# - low pass filter
#fc = 695. # cut-off frequency
#w = 0.985 #fc/frequ.max()
#b, a = signal.butter(5,w,'low')
#ufilt = signal.filtfilt(b, a, turb.u)
#vfilt = signal.filtfilt(b, a, turb.v)

#FFTufilt = np.fft.rfft(ufilt)

#turb2 = Turb(velPath,ufilt,vfilt)


#gradUx, gradVx, gradUy, gradVy = turb.calcVelGrad()

#tau11, tau22, tau12 = turb.calcTauijSmagorinsky()

#epsilongrad = turb.calcEpsilon('gradient')
#epsilonsmagorinsky = turb.calcEpsilon('smagorinsky')

#K = turb.calcK2DPIV()

#velVTKres = WVTK(velPath)
#velVTKres.save2DcellReynoldsVTK(raw.resPath,'turb',epsilongrad,epsilonsmagorinsky,K)


#******************************************************************************
## -- Uncertainty calculations
#******************************************************************************

varMag = turb.varU**2 + turb.varV**2
uncUMeanSq = np.mean(uncR**2,axis=2, keepdims=True)
uncSigma = varMag + uncUMeanSq
uncMeanVel = np.sqrt(uncSigma/velRaw.Ttot)
uncRuu = turb.uu*np.sqrt(2/velRaw.Ttot)

#******************************************************************************
## -- Save result in VTK format
#******************************************************************************

# - instantaneous
#velVTKres = WVTK(velPath)
#velVTKres.save2DcellVecTransientVTK(raw.resPath,'U',raw.U,raw.V)

# - mean
#VelMeanVTKres = WVTK(velPath)
#VelMeanVTKres.save2DcellVecVTK(raw.resPath,'<U>',turb.U,turb.V)

# - rms
#rmsVTKres = WVTK(velPath)
#rmsVTKres.save2DcellVecVTK(raw.resPath,'RMS',rmsUvtk,rmsVvtk)

#ReTensorVTKres = WVTK(velPath)
#ReTensorVTKres.save2DcellReynoldsVTK(raw.resPath,'ReStress',turb.uu,turb.vv,turb.uv)

#ReTensorVTKres2 = WVTK(velPath)
#ReTensorVTKres2.save2DcellReynoldsVTK(raw.resPath,'ReStressFilt',turb2.uu,turb2.vv,turb2.uv)

# - uncertainty
#uncVTKres = WVTK(velPath)
#uncVTKres.save2DcellVecTransientVTK(raw.resPath,'uncR',raw.uncR,raw.uncRpix)


#******************************************************************************
## -- Plot 2D line of variable
#******************************************************************************

plts = Plots(velPath)
plts.interpolation='bicubic'
plts.singleFramePlot(uncMeanVel/turb.magVel,r'$\overline{U}$ [m/s]',t=0, grid='on')

hline = plts.gethline(uncMeanVel[:,:,0], 20)
#vline = plts.getvline(uncMeanVel[:,:,0], 0)

uline = plts.gethline(turb.magVel,20)
Ruu = plts.gethline(turb.uu,20)
#uline2 = plts.gethline(turb.magVel,5)

# - Plot velocity magnitude comparing CFD and PIV with errors
CFDu = [CFD_x*-1000,CFD_velMag]
plts.plothLine(turb.magVel,20,r'$\overline{U}$ [m/s]',
               err=uncMeanVel,CFD=CFDu,xcorr=-2.5)

# - Plot Reynolds Stress uu CFD x PIV w errors
CFDuu = [CFD_x*-1000,CFD_uu]
plts.plothLine(turb.uu,20,r'Reynolds Stress $[m^2/s^2]$')
#plt.figure(figsize=(6,6),dpi=150)
#plt.plot(CFD_x*-1000,CFD_uu,'k',label='CFD')
#plt.errorbar(velRaw.xcoord[0,:]-2,Ruu,yerr=hline,fmt='o',ecolor='k',c='k',
#             ms=3,capsize=2,lw=1,label='PIV')
#plt.legend()
#plt.xlabel('Radius [mm]', size=16)
#plt.ylabel(r'$\overline{U}$ [m/s]', size=16)
#plt.xticks(size=16)
#plt.yticks(size=16)
#plt.title('$Y = 0.13 [m]$', size=18)

plt.show()

#******************************************************************************
print('\nEND crcPIV\n')
#******************************************************************************