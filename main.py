from logHelper import ExecuteWithLogs
from postprocessingHelper import GenerateRawFileFromPngs, Generate3dSplay, GetMaskFileName
from postprocessingHelper import JaccardCoefficient, DiceCoefficient, RunAnalisysPerRawFile
from postprocessingHelper import GenerateBoxPlotForRawFile, GenerateLinePlotForRawFile
from postprocessingHelper import GenerateBoxPlotForAllFiles, GenerateLinePlotForAllFiles
import os
import sys
import re
from PIL import Image
from shutil import copyfile

def RunAnalisys():   
    os.chdir("./data/analisys")        
    png_files = list(filter(lambda x: x.endswith(".png"), os.listdir("./result")))    
    CopyMasksForAnalisys(png_files)
    raw_filenames = []
    for png_file in png_files:
        raw_filename = png_file.replace(re.search(".raw_[\d]+.png", png_file).group(0), "")
        if (raw_filename not in raw_filenames):
            raw_filenames.append(raw_filename)
    coefs_per_file = []
    for file in raw_filenames:   
        coefs = ExecuteWithLogs("Analisys for file {0}".format(file), "log.txt", lambda _ = None: RunAnalisysPerRawFile(file))                 
        GenerateBoxPlotForRawFile(file, coefs)
        GenerateLinePlotForRawFile(file, coefs)
        coefs_per_file.append((file, coefs))   
    GenerateBoxPlotForAllFiles(coefs_per_file)
    GenerateLinePlotForAllFiles(coefs_per_file)

def PerformGenerations():       
    os.chdir("./data/generation")
    files = list(filter(lambda x: x.endswith(".mhd"), os.listdir(".")))
    ExecuteWithLogs("Raw file generation", "log.txt", lambda _ = None: GenerateRawFileFromPngs(files))   
    #ExecuteWithLogs("file 3D generation", "log.txt", lambda _ = None: Generate3dSplay(files))   

def CopyMasksForAnalisys(png_files):  
    mask_filenames = os.listdir("./source/mask")
    for i, png_file in enumerate(png_files):                
        mask_filename = GetMaskFileName(png_file,"./source/mask")
        copied = False
        if (mask_filename not in mask_filenames):
            copyfile("./source/mask/{0}".format(mask_filename), "./mask/{0}".format(mask_filename))
            copied = True
        print("{0}/{1} {2} {3}".format(i+1, len(png_files), png_file, "copied" if copied else ""))

#PerformGenerations()
RunAnalisys()


