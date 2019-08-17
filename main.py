from logHelper import ExecuteWithLogs
from postprocessingHelper import GenerateRawFileFromPngs, Generate3dSplay, GetMaskFileName
from postprocessingHelper import JaccardCoefficient, DiceCoefficient, RunAnalisysPerRawFile
from postprocessingHelper import GenerateBoxPlotForRawFile, GenerateLinePlotForRawFile
from postprocessingHelper import GenerateBoxPlotForAllFiles, GenerateLinePlotForAllFiles
import os
import sys
from PIL import Image

def RunAnalisys():
    os.chdir("./data/analisys")
    mhd_files = list(filter(lambda x: x.endswith(".mhd"), os.listdir("./result")))    
    coefs_per_file = []
    for file in mhd_files:   
        file = file.replace(".mhd","") 
        jaccard_coefs, dice_coefs = ExecuteWithLogs("Analisys for file {0}".format(file), "log.txt", lambda _ = None: RunAnalisysPerRawFile(file))                 
        GenerateBoxPlotForRawFile(file, jaccard_coefs, dice_coefs)
        GenerateLinePlotForRawFile(file, jaccard_coefs, dice_coefs)
        coefs_per_file.append((file, jaccard_coefs, dice_coefs))   
    GenerateBoxPlotForAllFiles(coefs_per_file)
    GenerateLinePlotForAllFiles(coefs_per_file)

def PerformGenerations():       
    os.chdir("./data/generation")
    files = list(filter(lambda x: x.endswith(".mhd"), os.listdir(".")))
    ExecuteWithLogs("Raw file generation", "log.txt", lambda _ = None: GenerateRawFileFromPngs(files))   
    #ExecuteWithLogs("file 3D generation", "log.txt", lambda _ = None: Generate3dSplay(files))   

#PerformGenerations()
RunAnalisys()
