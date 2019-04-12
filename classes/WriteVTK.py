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

from classes.SingleFrameData import SingleFrameData, np
from evtk.vtk import VtkFile, VtkImageData
#from progressbar import ProgressBar



class WVTK(SingleFrameData):
    '''
    Class to write results in VTK format for paraview
    '''
    def __init__(self,fRes):
        SingleFrameData.__init__(self,fRes)
        
        
    def save2DcellVecVTK(self, resPath, Uvtk, Vvtk):
        nx, ny, nz = self.cols, self.lins, 1
        origin, spacing = (0.0,0.0,0.0), (self.xscale,self.yscale,0.0001)
        start, end = (0,0,0), (nx, ny, nz)
        
        w = VtkFile(resPath + '/cellVec2D_img', VtkImageData)
        w.openGrid(start = start, end = end, origin = origin, spacing = spacing)
        w.openPiece( start = start, end = end)
        
        # Cell data
        zeroScalar = np.zeros([nx, ny, nz], dtype="float64", order='C')
        w.openData("Cell", vectors = "Velocities")
        w.addData("Velocities", (Uvtk, Vvtk, zeroScalar))
        w.closeData("Cell")
        
        w.closePiece()
        w.closeGrid()
        
        w.appendData(data = (Uvtk,Vvtk,zeroScalar))
        w.save()
        
        return 0
    
    def saveVTK(self,resPath,Uvtk,Vvtk):
        nx, ny, nz = self.cols, self.lins, 1
        origin, spacing = (0.0,0.0,0.0), (self.xscale,self.yscale,0.0001)
        start, end = (0,0,0), (nx, ny, nz)
        
        w = VtkFile(resPath + '/vecMask_img', VtkImageData)
        w.openGrid(start = start, end = end, origin = origin, spacing = spacing)
        w.openPiece( start = start, end = end)
        
        # Point data
        #temp = np.random.rand(npoints)
        #vx = vy = vz = np.zeros([nx + 1, ny + 1, nz + 1], dtype="float64", order = 'F')
        #w.openData("Point", scalars = "Temperature", vectors = "Velocity")
        #w.addData("Temperature", temp)
        #w.addData("Velocity", (vx,vy,vz))
        #w.closeData("Point")
        
        # Cell data
        zeroScalar = np.zeros([nx, ny, nz], dtype="float64", order='C')
        w.openData("Cell", scalars = "Pressure", vectors = "Velocities")
        #w.openData("Cell", vectors = "Velocities")
        w.addData("Pressure", zeroScalar)
        w.addData("Velocities", (Uvtk, Vvtk, zeroScalar))
        w.closeData("Cell")
        
        w.closePiece()
        w.closeGrid()
        
        w.appendData(data = zeroScalar)
        w.appendData(data = (Uvtk,Vvtk,zeroScalar))
        w.save()
        
        return 0
