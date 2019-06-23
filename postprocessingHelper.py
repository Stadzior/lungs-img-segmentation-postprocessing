import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
        ct_image_layered = Build3dByteArrayFromPngs(fileName)

        with open("{0}.raw".format(fileName), "wb") as rawFile:
            rawFile.write(ct_image_str)

    # fig = plt.figure()
    # plt.imshow(ct_image, cmap=plt.cm.gray)
    # plt.show()
    
# fig = plt.figure()
# ax = fig.gca(projection='3d')

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

# # Make legend, set axes limits and labels
# ax.legend()
# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)
# ax.set_zlim(0, 1)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Customize the view angle so it's easier to see that the scatter points lie
# # on the plane y=0
# ax.view_init(elev=20., azim=-35)

# plt.show()
