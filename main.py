from logHelper import ExecuteWithLogs
from postprocessingHelper import GenerateRawFileFromPngs, Generate3dSplay, GetMaskFileName
from postprocessingHelper import JaccardCoefficient, DiceCoefficient, RunAnalisysPerRawFile
from postprocessingHelper import GenerateBoxPlotForRawFile, GenerateLinePlotForRawFile
from postprocessingHelper import GenerateBoxPlotForAllFiles, GenerateLinePlotForAllFiles
from postprocessingHelper import ExtractRawFileNamesFromPngFiles
import os
import sys
import re
from PIL import Image
from shutil import copyfile, rmtree

def RunAnalisys():   
    os.chdir("./data/analisys")        
    png_files = list(filter(lambda x: x.endswith(".png"), os.listdir("../result")))    
    raw_files = ExtractRawFileNamesFromPngFiles(png_files)
    coefs_per_file = []
    for i, raw_file in enumerate(raw_files):   
        print("{0}/{1} {2}".format(i+1, len(raw_files), raw_file))
        coefs = ExecuteWithLogs("Analisys for file {0}".format(raw_file), "log.txt", lambda _ = None: RunAnalisysPerRawFile(raw_file))                 
        GenerateBoxPlotForRawFile(raw_file, coefs)
        GenerateLinePlotForRawFile(raw_file, coefs)
        coefs_per_file.append((raw_file, coefs))   
    for raw_file, coefs in coefs_per_file:
        jaccard_raw_file = sum(list(map(lambda x: x[1], coefs)))/len(coefs)
        dice_raw_file = sum(list(map(lambda x: x[2], coefs)))/len(coefs)
        print("{0} Jaccard: {1} Dice: {2}".format(raw_file, jaccard_raw_file, dice_raw_file))

    GenerateBoxPlotForAllFiles(coefs_per_file)
    GenerateLinePlotForAllFiles(coefs_per_file)

def PerformGenerations():       
    os.chdir("./data/generation")
    png_files = list(filter(lambda x: x.endswith(".png"), os.listdir("../result")))    
    raw_files = ExtractRawFileNamesFromPngFiles(png_files)
    for i, raw_file in enumerate(raw_files):        
        print("{0}/{1} {2}".format(i+1, len(raw_files), raw_file))
        ExecuteWithLogs("Raw file generation {0}".format(raw_file), "log.txt", lambda _ = None: GenerateRawFileFromPngs(raw_file))   

RunAnalisys()
#PerformGenerations()
