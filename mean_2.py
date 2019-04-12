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
import numpy as np

#******************************************************************************
#******************************************************************************

print('\nStart mean_2\n')    

#******************************************************************************
## -- Main
#******************************************************************************

Umean = np.mean(raw.U,axis=2, keepdims=True)
Vmean = np.mean(raw.V,axis=2, keepdims=True)

Uvtk = np.ascontiguousarray(np.rot90(Umean,k=1, axes=(1,0)))
Vvtk = np.ascontiguousarray(np.rot90(Vmean,k=1, axes=(1,0)))

## -- Save result in VTK format
WVTK(raw.files,raw.resPath,Uvtk,Vvtk)

#******************************************************************************
#******************************************************************************

print('\nEND mean_2\n')