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
from classes.WriteVTK import WVTK
from classes.Turbulence import Turb
#import numpy as np
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
uncRaw.printCoordInfos()


#******************************************************************************
## -- Seeding tracers
#******************************************************************************

tracer = SiO2()
#tracer.graphResponse(ymin=0.8)

#******************************************************************************
## -- Turbulence calculations
#******************************************************************************

#turb = Turb(raw.files,raw.U,raw.V)


#FFTu = np.fft.rfft(turb.u[90,30,:])
#frequ = np.fft.rfftfreq(raw.Raw.Ttot,1./fa)


# - low pass filter
#fc = 695. # cut-off frequency
#w = 0.985 #fc/frequ.max()
#b, a = signal.butter(5,w,'low')
#ufilt = signal.filtfilt(b, a, turb.u)
#vfilt = signal.filtfilt(b, a, turb.v)

#FFTufilt = np.fft.rfft(ufilt)

#turb2 = Turb(raw.files,ufilt,vfilt)


#gradUx, gradVx, gradUy, gradVy = turb.calcVelGrad()

#tau11, tau22, tau12 = turb.calcTauijSmagorinsky()

#epsilongrad = turb.calcEpsilon('gradient')
#epsilonsmagorinsky = turb.calcEpsilon('smagorinsky')

#K = turb.calcK2DPIV()

#velVTKres = WVTK(raw.files)
#velVTKres.save2DcellReynoldsVTK(raw.resPath,'turb',epsilongrad,epsilonsmagorinsky,K)


#******************************************************************************
## -- Save result in VTK format
#******************************************************************************

# - instantaneous
#velVTKres = WVTK(raw.files)
#velVTKres.save2DcellVecTransientVTK(raw.resPath,'U',raw.U,raw.V)

# - mean
#VelMeanVTKres = WVTK(raw.files)
#VelMeanVTKres.save2DcellVecVTK(raw.resPath,'<U>',turb.U,turb.V)

# - rms
#rmsVTKres = WVTK(raw.files)
#rmsVTKres.save2DcellVecVTK(raw.resPath,'RMS',rmsUvtk,rmsVvtk)

#ReTensorVTKres = WVTK(raw.files)
#ReTensorVTKres.save2DcellReynoldsVTK(raw.resPath,'ReStress',turb.uu,turb.vv,turb.uv)

#ReTensorVTKres2 = WVTK(raw.files)
#ReTensorVTKres2.save2DcellReynoldsVTK(raw.resPath,'ReStressFilt',turb2.uu,turb2.vv,turb2.uv)

# - uncertainty
#uncVTKres = WVTK(raw.files)
#uncVTKres.save2DcellVecTransientVTK(raw.resPath,'uncR',raw.uncR,raw.uncRpix)


#******************************************************************************
## -- Plot 2D line of variable
#******************************************************************************



extent = [velRaw.xmin,velRaw.xmax,velRaw.ymin,velRaw.ymax]
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
ax = plt.gca()
#plt.figure(figsize=(5.5,6),dpi=150)
im = ax.imshow(v[:,:,0], cmap='jet', interpolation='bicubic',extent=extent)
plt.xlabel('Radius [mm]', fontsize=16)
plt.ylabel(r'y [mm]', fontsize=16)
#plt.xticks(np.arange(velRaw.cols),size=16)
plt.yticks(size=16)
cbar = ax.figure.colorbar(im)
cbar.ax.tick_params(labelsize=16)
cbar.set_label(r'$\overline{U}$ [m/s]',size=16)
#cbar.set_label(r'$\overline{U}$ [m/s]',rotation=0,y=1.05,labelpad=-17,size=16)
plt.show()


#******************************************************************************
print('\nEND crcPIV\n')
#******************************************************************************