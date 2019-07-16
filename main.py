from logHelper import ExecuteWithLogs
from postprocessingHelper import GenerateRawFileFromPngs, Generate3dSplay, GetMaskFileName, JaccardCoefficient, DiceCoefficient
import os
import sys
from PIL import Image

def RunAnalisys():
    log_file_path = "analisys/log.txt"
    files = list(filter(lambda x: x.endswith(".png"), os.listdir("./analisys/result")))    
    for file in files:
        mask = Image.open("./analisys/mask/{0}".format(GetMaskFileName(file, "./analisys/mask")), mode='r')
        result = Image.open("./analisys/result/{0}".format(file), mode='r')
        jaccardCoefficient = JaccardCoefficient(mask, result)
        print("Jaccard's coefficient for {0}: {1}".format(file, jaccardCoefficient))  
        print("Dice's coefficient for {0}: {1}".format(file, DiceCoefficient(jaccardCoefficient)))

def PerformGenerations():
    log_file_path = "generation/log.txt"
    files = list(filter(lambda x: x.endswith(".mhd"), os.listdir("./generation")))
    ExecuteWithLogs("Raw file generation", log_file_path, lambda _ = None: GenerateRawFileFromPngs(files))   
    #ExecuteWithLogs("file 3D generation", log_file_path, lambda _ = None: Generate3dSplay(files))   

os.chdir("./data")
#PerformGenerations()
RunAnalisys()

