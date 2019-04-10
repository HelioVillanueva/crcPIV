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

from classes.ReadData import ReadData
from glob import glob
#import numpy as np

#******************************************************************************
#******************************************************************************


print('\nStart 1readRaw\n')    
#******************************************************************************
## -- Main
#******************************************************************************
resPath = '../Res0-vecMask'
files = glob(resPath + '/*')


## -- Read PIV data. If python format already present read it instead
Raw = ReadData(files)

U,V = Raw.read(resPath)


Raw.printCoordInfos()

print('END 1readRaw\n')