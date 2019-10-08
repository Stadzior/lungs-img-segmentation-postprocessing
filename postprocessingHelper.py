import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib as mpl
import base64
import io
import re

LAYER_RANGE = (251,308)
TARGET_SIZE = (512,512)

def GenerateRawFileFromPngs(raw_file, dir_path):  
    png_files = FindPngFilesWithFileName(raw_file, dir_path)
    ct_image_layered = []
    for i in range(LAYER_RANGE[0], LAYER_RANGE[1]):
        png_file_name = next((x[1] for x in png_files if x[0] == i), None)        
        if png_file_name is not None:
            img = Image.open("{0}/{1}".format(dir_path, png_file_name), mode='r')
            img = img.convert('L')
        else:
            img = Image.new('L', TARGET_SIZE)
        img_array = np.asarray(img)
        img_str = img_array.tostring()
        ct_image_layered.append(img_str)
    ct_image_str = b''.join(ct_image_layered)  
    with open("{0}.raw".format(raw_file), "wb") as rawFile:
        rawFile.write(ct_image_str)

def FindPngFilesWithFileName(fileName, dir_path = "."):
    png_filenames = filter(lambda x: x.startswith(fileName) and x.endswith(".png"), os.listdir(dir_path))
    extractIndexFromFileName = lambda x: (int(re.search("_[\d]+.png", x).group(0).replace("_", "").replace(".png", "")))
    png_files = [(extractIndexFromFileName(x), x) for x in png_filenames]
    png_files.sort(key = lambda x: x[0])
    return png_files

def JaccardCoefficient(mask, result):
    intersection = np.logical_and(mask, result)
    union = np.logical_or(mask, result)    
    return np.sum(intersection) / np.sum(union)
  
def DiceCoefficient(mask, result):    
    mask = np.asarray(mask).astype(np.bool)
    result = np.asarray(result).astype(np.bool)
    intersection = np.logical_and(mask, result)
    return (2. * np.sum(intersection)) / (np.sum(mask) + np.sum(result))

def GetMaskFileName(image_filename, mask_source_path):
    return list(filter(lambda x: x.replace("_Delmon_CompleteMM", "").startswith(image_filename) and x.endswith(".png"), os.listdir(mask_source_path)))[0]

def GenerateBoxPlotForRawFile(file, coefs):    
    jaccard_coefs = list(map(lambda x: x[1], coefs))
    dice_coefs = list(map(lambda x: x[2], coefs))
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.set(xlabel='coefs', ylabel='value',
        title='Jaccard and Dice coefs boxplot for {0}'.format(file))
    ax.boxplot([jaccard_coefs, dice_coefs])
    fig.savefig("./plots/boxplot_{0}.png".format(file), bbox_inches='tight')
    plt.clf()

def GenerateLinePlotForRawFile(file, coefs):
    x = range(LAYER_RANGE[0], LAYER_RANGE[1])
    jaccard_coefs = []
    dice_coefs = []
    for i in x:
        jaccard_coefs.append(next((x[1] for x in coefs if x[0] == i), None))
        dice_coefs.append(next((x[2] for x in coefs if x[0] == i), None))
    fig, ax = plt.subplots()
    ax.plot(x, jaccard_coefs, "bo-", label = "Jaccard")
    ax.plot(x, dice_coefs, "ro-", label = "Dice")
    ax.set(xlabel='layer position', ylabel='value',
        title='Jaccard and Dice coefs per layer for {0}'.format(file))
    ax.grid()
    fig.savefig("./plots/lineplot_{0}.png".format(file))
    plt.clf()
def GenerateBoxPlotForAllFiles(coefs_per_file):
    coefs = [item for sublist in list(map(lambda x: x[1], coefs_per_file)) for item in sublist]    
    jaccard_coefs = list(map(lambda x: x[1], coefs))
    dice_coefs = list(map(lambda x: x[2], coefs)) 
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.set(xlabel='coefs', ylabel='value',
        title='Jaccard and Dice coefs boxplot for all')
    ax.boxplot([jaccard_coefs, dice_coefs])
    fig.savefig("./plots/boxplot_all.png", bbox_inches='tight')
    plt.clf()

def GenerateLinePlotForAllFiles(coefs_per_file):
    x = range(LAYER_RANGE[0], LAYER_RANGE[1])
    coefs = [item for sublist in list(map(lambda x: x[1], coefs_per_file)) for item in sublist]  
    jaccard_coefs = []
    dice_coefs = []
    for i in x:
        coefs_for_layer = list(filter(lambda x: x[0] == i, coefs))
        if (any(coefs_for_layer)):
            jaccard_coef = sum(list(map(lambda x: x[1], coefs_for_layer)))/len(coefs_for_layer)
            jaccard_coefs.append(jaccard_coef)
            dice_coef = sum(list(map(lambda x: x[2], coefs_for_layer)))/len(coefs_for_layer)
            dice_coefs.append(dice_coef)
        else:
            jaccard_coefs.append(None)
            dice_coefs.append(None)
    fig, ax = plt.subplots()
    ax.plot(x, jaccard_coefs, "bo-", label = "Jaccard")
    ax.plot(x, dice_coefs, "ro-", label = "Dice")
    ax.set(xlabel='layer position', ylabel='value',
        title='Jaccard and Dice coefs per layer for all')
    ax.grid()
    fig.savefig("./plots/lineplot_all.png")
    plt.clf()

def RunAnalisysPerRawFile(file):
    png_files = FindPngFilesWithFileName(file, "../result")
    coefs = []
    for index, png_file in png_files:
        jaccard_coef, dice_coef = RunAnalisysPerPngFile(png_file)
        coefs.append((index, jaccard_coef, dice_coef))
    return coefs

def RunAnalisysPerPngFile(file):
    mask = Image.open("./mask/{0}".format(GetMaskFileName(file, "./mask")), mode='r')
    result = Image.open("../result/{0}".format(file), mode='r')
    jaccard_coef = JaccardCoefficient(mask, result)
    dice_coef = DiceCoefficient(mask, result)
    print("Jaccard's coefficient for {0}: {1}".format(file, jaccard_coef))  
    print("Dice's coefficient for {0}: {1}".format(file, dice_coef))
    return (jaccard_coef, dice_coef)

def ExtractRawFileNamesFromPngFiles(png_files):
    raw_filenames = []
    for png_file in png_files:
        raw_filename = png_file.replace(re.search(".raw_[\d]+.png", png_file).group(0), "")
        if (raw_filename not in raw_filenames):
            raw_filenames.append(raw_filename)
    return raw_filenames