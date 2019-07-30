#!/usr/bin/env python
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
"""

import readRaw_1 as raw
from classes.WriteVTK import WVTK
from classes.Turbulence import Turb
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#******************************************************************************
#******************************************************************************

print('\nStart mean_2\n')    

#******************************************************************************
## -- Main
#******************************************************************************

fa = 1400. # - aquisition frequency

turb = Turb(raw.files,raw.U,raw.V)


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


## -- Save result in VTK format
# - instantaneous
velVTKres = WVTK(raw.files)
velVTKres.save2DcellVecTransientVTK(raw.resPath,'U',raw.U,raw.V)

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

#******************************************************************************
#******************************************************************************

print('\nEND mean_2\n')