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
        z = list(range(0, zlim))
        for zIndex in range (0, zlim):
            print("{0}/{1}".format(zIndex+1, zlim+1))
            verticies = []
            for yIndex in range(0,ylim):
                x = [i for i, value in enumerate(ct_image_layered[zIndex][yIndex]) if value > 0]
                if (x):
                    y = [yIndex] * len(x)                 
                    verticies.append(list(zip(x,y)))
            poly = PolyCollection(verticies)
            poly.set_alpha(0.95)
            ax.add_collection3d(poly, zs=zIndex)   
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
# fig = plt.figure()

# # Plot a sin curve using the x and y axes.
# x = np.linspace(0, 1, 100)
# y = np.sin(x * 2 * np.pi) / 2 + 0.5
# ax.plot(x, y, zs=0, zdir='z', label='curve in (x,y)')

# # Plot scatterplot data (20 2D points per colour) on the x and z axes.
# colors = ('r', 'g', 'b', 'k')
# x = np.random.sample(20*len(colors))
# y = np.random.sample(20*len(colors))
# c_list = []
# for c in colors:
#     c_list.append([c]*20)
# # By using zdir='y', the y value of these points is fixed to the zs value 0
# # and the (x,y) points are plotted on the x and z axes.
# ax.scatter(x, y, zs=0, zdir='y', c=c_list, label='points in (x,z)')



# plt.show()
