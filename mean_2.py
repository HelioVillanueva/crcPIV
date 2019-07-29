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

#******************************************************************************
#******************************************************************************

print('\nStart mean_2\n')    

#******************************************************************************
## -- Main
#******************************************************************************

#Umean = np.mean(raw.U,axis=2, keepdims=True)
#Vmean = np.mean(raw.V,axis=2, keepdims=True)
Umean = raw.U
Vmean = raw.V

#uu = rmsUvtk*rmsUvtk
#vv = rmsVvtk*rmsVvtk
#uv = rmsUvtk*rmsVvtk



## -- Save result in VTK format
VelMeanVTKres = WVTK(raw.files)
VelMeanVTKres.save2DcellVecTransientVTK(raw.resPath,'velMean',Umean,Vmean)

rmsVTKres = WVTK(raw.files)
#rmsVTKres.save2DcellVecVTK(raw.resPath,'RMS',rmsUvtk,rmsVvtk)

ReTensorVTKres = WVTK(raw.files)
#ReTensorVTKres.save2DcellReynoldsVTK(raw.resPath,'ReStress',uu,vv,uv)

#******************************************************************************
#******************************************************************************

print('\nEND mean_2\n')