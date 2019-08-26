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

from classes.SingleFrameData import SingleFrameData, np, re
from progressbar import ProgressBar

class ReadData(SingleFrameData):
    '''
    Class to read all timesteps from Dantec Data\n
    fRes list of raw PIV files from Dantec\n
    resPath: Path of raw PIV files from Dantec\n
    '''
    def __init__(self,resPath):
        SingleFrameData.__init__(self,resPath)
        self.Ttot = len(self.files)
        

    
    def readVar(self,varXname,varYname):
        '''Method to read the raw data if there is no "var".npy file
        Return varX,varY
        '''
        varXnametratado = re.sub('\[.*\]','',varXname).replace(" ","")
        varYnametratado = re.sub('\[.*\]','',varYname).replace(" ","")
        
        try:
            varX = np.load(self.resPath + '/' + varXnametratado + '.npy')
            print('Reading PIV data of ' + varXname + ' in python format\n')
            varY = np.load(self.resPath + '/' + varYnametratado + '.npy')
            
        except:
            print('Reading PIV raw files for ' + varXname)
        
            #varX,varY = self.readVarTimeSeries(varXname,varYname)
            varX,varY = self.readFrameVariable(0,varXname,varYname)
            
            print('Saving PIV data in python format')
            np.save(self.resPath + '/' + varXnametratado,varX)
            np.save(self.resPath + '/' + varYnametratado,varY)
            
        return varX,varY
        
    def read1VarTimeSeries(self,varName):
        
        varXnametratado = re.sub('\[.*\]','',varName).replace(" ","")
        
        print('Reading variable: ' + str(varXnametratado))
        
        try:
            varX = np.load(self.resPath + '/' + varXnametratado + '.npy')
            print('Reading PIV data of ' + varName + ' in python format\n')
            
        except:
            print('Generating variable matrices')
            varX = np.zeros((self.lins, self.cols, self.Ttot))
            
            print('Reading PIV Frames - Variable components')
            pbar = ProgressBar()
            pbar.start()
            
            ## -- Loop over all files/times
            for time,name in enumerate(self.fRes):
                if time==0:
                    perc = 0.
                else:
                    perc = time/float(self.Ttot)*100.
                    
                varX[:,:,time] = self.readFrame1Variable(time,varName)
                
                pbar.update(perc)
                
            pbar.finish()
            
            print('Saving PIV data in python format')
            np.save(self.resPath + '/' + varXnametratado,varX)
            print('Done saving')
        
        return varX
    
    def read2VarTimeSeries(self,varXname,varYname):
        
        varXnametratado = re.sub('\[.*\]','',varXname).replace(" ","")
        varYnametratado = re.sub('\[.*\]','',varYname).replace(" ","")
        
        print('Reading variables: ' + str(varXnametratado) + ' & ' + str(varYnametratado))
        
        try:
            varX = np.load(self.resPath + '/' + varXnametratado + '.npy')
            print('Reading PIV data of ' + varXname + ' in python format\n')
            varY = np.load(self.resPath + '/' + varYnametratado + '.npy')
            
        except:
            print('Generating variable matrices')
            varX = np.zeros((self.lins, self.cols, self.Ttot))
            varY = np.zeros((self.lins, self.cols, self.Ttot))
            
            print('Reading PIV Frames - Variable components')
            pbar = ProgressBar()
            pbar.start()
            
            ## -- Loop over all files/times
            for time,name in enumerate(self.fRes):
                if time==0:
                    perc = 0.
                else:
                    perc = time/float(self.Ttot)*100.
                    
                varX[:,:,time],varY[:,:,time] = self.readFrameVariable(time,varXname,varYname)
                
                pbar.update(perc)
                
            pbar.finish()
            
            print('Saving PIV data in python format')
            np.save(self.resPath + '/' + varXnametratado,varX)
            np.save(self.resPath + '/' + varYnametratado,varY)
            print('Done saving')
        
        return varX,varY
    
    def read1UncTimeSeries(self,varXname):
        
        varXnametratado = re.sub('\[.*\]','',varXname).replace(" ","")
        
        print('Reading variables: ' + str(varXnametratado))
        
        try:
            varX = np.load(self.resPath + '/' + 'uncR' + '.npy')
            #varX = np.load(self.resPath + '/' + varXnametratado + '.npy')
            print('Reading PIV data of ' + varXname + ' in python format\n')
            
        except:
            print('Generating variable matrices')
            varX = np.zeros((self.lins, self.cols, self.Ttot))
            
            print('Reading PIV Frames - Variable components')
            pbar = ProgressBar()
            pbar.start()
            
            ## -- Loop over all files/times
            for time,name in enumerate(self.fRes):
                if time==0:
                    perc = 0.
                else:
                    perc = time/float(self.Ttot)*100.
                    
                varX[:,:,time] = self.readFrame1Variable(time,varXname)
                
                pbar.update(perc)
                
            pbar.finish()
            
            print('Saving PIV data in python format')
            np.save(self.resPath + '/' + 'uncR',varX)
            print('Done saving')
        
        return varX
    
    def readUncTimeSeries(self,varXname,varYname):
        
        varXnametratado = re.sub('\[.*\]','',varXname).replace(" ","")
        varYnametratado = re.sub('\[.*\]','',varYname).replace(" ","")
        
        print('Reading variables: ' + str(varXnametratado) + ' & ' + str(varYnametratado))
        
        try:
            varX = np.load(self.resPath + '/' + 'uncR' + '.npy')
            #varX = np.load(self.resPath + '/' + varXnametratado + '.npy')
            print('Reading PIV data of ' + varXname + ' in python format\n')
            varY = np.load(self.resPath + '/' + 'uncRpix' + '.npy')
            #varY = np.load(self.resPath + '/' + varYnametratado + '.npy')
            
        except:
            print('Generating variable matrices')
            varX = np.zeros((self.lins, self.cols, self.Ttot))
            varY = np.zeros((self.lins, self.cols, self.Ttot))
            
            print('Reading PIV Frames - Variable components')
            pbar = ProgressBar()
            pbar.start()
            
            ## -- Loop over all files/times
            for time,name in enumerate(self.fRes):
                if time==0:
                    perc = 0.
                else:
                    perc = time/float(self.Ttot)*100.
                    
                varX[:,:,time],varY[:,:,time] = self.readFrameVariable(time,varXname,varYname)
                
                pbar.update(perc)
                
            pbar.finish()
            
            print('Saving PIV data in python format')
            np.save(self.resPath + '/' + 'uncR',varX)
            np.save(self.resPath + '/' + 'uncRpix',varY)
            #np.save(self.resPath + '/' + varXnametratado,varX)
            #np.save(self.resPath + '/' + varYnametratado,varY)
            print('Done saving')
        
        return varX,varY

## OLD NOT USED
#    def read(self):
#        '''Method to read the raw data if there is no U.py ou V.py file
#        Return U,V
#        '''
#        try:
#            U = np.load(self.resPath + '/U.npy')
#            print('Reading PIV data in python format\n')
#            V = np.load(self.resPath + '/V.npy')
#            Uf,Vf = self.readFrameVelocities(0)
#            
#        except:
#            print('Reading PIV raw files')
#        
#            Uf,Vf = self.readFrameVelocities(0)
#            U,V = self.readVelTimeSeries()
#            
#            print('Saving PIV data in python format')
#            np.save(self.resPath + '/U',U)
#            np.save(self.resPath + '/V',V)
#            
#        return U,V
        
#    def readVelTimeSeries(self):
#        
#        print('Generating velocities matrices')
#        U = np.zeros((self.lins, self.cols, self.Ttot))
#        V = np.zeros((self.lins, self.cols, self.Ttot))
#        
#        print('Reading PIV Frames - Velocity components')
#        pbar = ProgressBar()
#        pbar.start()
#        
#        ## -- Loop over all files/times
#        for time,name in enumerate(self.fRes):
#            
#            if time==0:
#                perc = 0.
#            else:
#                perc = time/float(self.Ttot)*100.
#            
#            U[:,:,time],V[:,:,time] = self.readFrameVelocities(time)
#            
#            pbar.update(perc)
#        
#        pbar.finish()
#        
#        return U,V