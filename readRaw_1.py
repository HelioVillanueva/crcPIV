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

#******************************************************************************
#******************************************************************************

print('\nStart readRaw_1\n')    

#******************************************************************************
## -- Main
#******************************************************************************

## -- Path to the PIV results files and store in "files" list of names
resPath = '../Res0-vecMask'
files = glob(resPath + '/*')


## -- Instance of class with PIV results infos
Raw = ReadData(files)

## -- Read PIV data. If python format already present read it instead
U,V = Raw.read(resPath)

## -- Print infos about coordinates and size of Field-of-View (FOV)
Raw.printCoordInfos()

#******************************************************************************
#******************************************************************************

print('\nEND readRaw_1\n')