from logHelper import ExecuteWithLogs
from postprocessingHelper import GenerateRawFileFromPngs, Generate3dSplay, GetMaskFileName
from postprocessingHelper import JaccardCoefficient, DiceCoefficient, RunAnalisysPerRawFile
import os
import sys
from PIL import Image

def RunAnalisys():
    os.chdir("./data/analisys")
    mhd_files = list(filter(lambda x: x.endswith(".mhd"), os.listdir("./result")))    
    for file in mhd_files:
        ExecuteWithLogs("Analisys for file {0}".format(file), "log.txt", lambda _ = None: RunAnalisysPerRawFile(file))          

def PerformGenerations():       
    os.chdir("./data/generation")
    files = list(filter(lambda x: x.endswith(".mhd"), os.listdir(".")))
    ExecuteWithLogs("Raw file generation", "log.txt", lambda _ = None: GenerateRawFileFromPngs(files))   
    #ExecuteWithLogs("file 3D generation", "log.txt", lambda _ = None: Generate3dSplay(files))   

#PerformGenerations()
RunAnalisys()
