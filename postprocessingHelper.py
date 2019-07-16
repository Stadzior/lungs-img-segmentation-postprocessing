import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import base64
import io
import re

def GenerateRawFileFromPngs(files):  
    for i, file in enumerate(files):
        print("{0}/{1} {2}".format(i, len(files), file))
        filename = file.replace(".mhd","")
        png_files = FindPngFilesWithFileName(filename)
        ct_image_layered = []
        for (index, png_file_name) in png_files:
            img = Image.open(png_file_name, mode='r')
            img_array = np.asarray(img)
            img_str = img_array.tostring()
            ct_image_layered.append(img_str) 
        ct_image_str = b''.join(ct_image_layered)  
        with open("{0}.raw".format(filename), "wb") as rawFile:
            rawFile.write(ct_image_str)

def Generate3dSplay(files):  
    for i, file in enumerate(files):
        print("{0}/{1} {2}".format(i, len(files), file))
        filename = file.replace(".mhd","")
        png_filenames = FindPngFilesWithFileName(filename)
        ct_image_layered = []
        for pngFile in png_filenames:
            img = Image.open(pngFile, mode='r')
            img_array = np.asarray(img)
            xlim, ylim = img.size
            xlim = xlim-1
            ylim = ylim-1
            ct_image_layered.append(img_array) 
        zlim = len(ct_image_layered)-1
        #create figure
        fig = plt.figure()
        ax = fig.gca(projection='3d')
    
        # plotting
        print("before plotting")
        for z in range (0, zlim):
            print("{0}/{1}".format(z+1, zlim+1))
            verticies = []
            for x in range (0, xlim):
                for y in range (0, ylim):
                    if (ct_image_layered[z][y][x] > 0 and CheckIfNotRedundantVertex(ct_image_layered[z], x, y)):
                        verticies.append((x,y))
            if (verticies):
                poly = PolyCollection([verticies])
                ax.add_collection3d(poly, zs=z)   
        print("polygons built")

        # Set axes limits and labels
        ax.set_xlim3d(0, xlim)
        ax.set_ylim3d(0, ylim)
        ax.set_zlim3d(0, zlim)
        ax.set_xlabel('Coronal')
        ax.set_ylabel('Sagittal')
        ax.set_zlabel('Axial')

        # Customize the view angle so it's easier to see that the scatter points lie on the plane y=0
        ax.view_init(elev=20., azim=-35)
        plt.show()
        print("showed")

def FindPngFilesWithFileName(fileName):
    png_filenames = filter(lambda x: x.startswith(fileName) and x.endswith(".png"), os.listdir("."))
    extractIndexFromFileName = lambda x: (int(re.search("_[\d]+.png", x).group(0).replace("_", "").replace(".png", "")))
    png_files = [(extractIndexFromFileName(x), x) for x in png_filenames]
    png_files.sort(key = lambda x: x[0])
    return png_files

def CheckIfNotRedundantVertex(layer, x, y):
    x_max, y_max = layer.shape
    return (x > 0 and y > 0 and layer[x-1][y-1] == 0) or (y > 0 and layer[x][y-1] == 0) or (x < x_max - 1 and y > 0 and layer[x+1][y-1] == 0) or (x < x_max - 1 and layer[x+1][y] == 0) or (x < x_max - 1 and y < y_max - 1 and layer[x+1][y+1] == 0) or (y < y_max - 1 and layer[x][y+1] == 0) or (x > 0 and y < y_max - 1 and layer[x-1][y+1] == 0) or (x > 0 and layer[x-1][y] == 0)

def JaccardCoefficient(mask, result):
    intersection = np.logical_and(mask, result)
    union = np.logical_or(mask, result)    
    return np.sum(intersection) / np.sum(union)
  
def DiceCoefficient(mask, result):    
    intersection = np.logical_and(mask, result)
    return (2 * np.sum(intersection)) / (np.sum(mask) + np.sum(result))

def GetMaskFileName(image_filename, mask_source_path):
    return list(filter(lambda x: x.replace("_Delmon_CompleteMM", "").startswith(image_filename) and x.endswith(".png"), os.listdir(mask_source_path)))[0]