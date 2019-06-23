import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import base64
import io

def GenerateRawFileFromPngs():  
    for mhdFile in filter(lambda x: x.endswith(".mhd"), os.listdir(".")):
        fileName = mhdFile.replace(".mhd","")
        ct_image_layered = []
        for pngFile in filter(lambda x: x.startswith(fileName) and x.endswith(".png"), os.listdir(".")):
            img = Image.open(pngFile, mode='r')
            img_array = np.asarray(img)
            img_str = img_array.tostring()
            ct_image_layered.append(img_str) 
        ct_image_str = b''.join(ct_image_layered)  
        with open("{0}.raw".format(fileName), "wb") as rawFile:
            rawFile.write(ct_image_str)

def Generate3dSplay():  
    for mhdFile in filter(lambda x: x.endswith(".mhd"), os.listdir(".")):
        fileName = mhdFile.replace(".mhd","")
        ct_image_layered = []
        for pngFile in filter(lambda x: x.startswith(fileName) and x.endswith(".png"), os.listdir(".")):
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
                        #verticies.append(list(zip(x,y))) <--- to be fixed
            poly = PolyCollection(verticies)
            poly.set_alpha(0.95)
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

def CheckIfNotRedundantVertex(layer, x, y):
    xMax, yMax = layer.shape
    return (x > 0 and y > 0 and layer[x-1][y-1] == 0) or (y > 0 and layer[x][y-1] == 0) or (x < xMax - 1 and y > 0 and layer[x+1][y-1] == 0) or (x < xMax - 1 and layer[x+1][y] == 0) or (x < xMax - 1 and y < yMax - 1 and layer[x+1][y+1] == 0) or (y < yMax - 1 and layer[x][y+1] == 0) or (x > 0 and y < yMax - 1 and layer[x-1][y+1] == 0) or (x > 0 and layer[x-1][y] == 0)