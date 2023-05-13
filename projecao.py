import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#%matplotlib inline
import numpy as np
from functions import *

def init_cam(initial_point=[35,-5,8]):
    e1 = np.array([[1], [0], [0], [0]])  # X
    e2 = np.array([[0], [1], [0], [0]])  # Y
    e3 = np.array([[0], [0], [1], [0]])  # Z
    base = np.hstack((e1, e2, e3))
    point = np.array([[0],[0],[0],[1]])

    cam = np.hstack((base, point))
    M = translate(initial_point[0], initial_point[1], initial_point[2]) @ z_rotation(90) @ x_rotation(-90)
    return M@cam, M

def init_obj():
    house = np.array([[0, 0, 0],
                      [0, -10.0000, 0],
                      [0, -10.0000, 12.0000],
                      [0, -10.4000, 11.5000],
                      [0, -5.0000, 16.0000],
                      [0, 0, 12.0000],
                      [0, 0.5000, 11.4000],
                      [0, 0, 12.0000],
                      [0, 0, 0],
                      [-12.0000, 0, 0],
                      [-12.0000, -5.0000, 0],
                      [-12.0000, -10.0000, 0],
                      [0, -10.0000, 0],
                      [0, -10.0000, 12.0000],
                      [-12.0000, -10.0000, 12.0000],
                      [-12.0000, 0, 12.0000],
                      [0, 0, 12.0000],
                      [0, -10.0000, 12.0000],
                      [0, -10.5000, 11.4000],
                      [-12.0000, -10.5000, 11.4000],
                      [-12.0000, -10.0000, 12.0000],
                      [-12.0000, -5.0000, 16.0000],
                      [0, -5.0000, 16.0000],
                      [0, 0.5000, 11.4000],
                      [-12.0000, 0.5000, 11.4000],
                      [-12.0000, 0, 12.0000],
                      [-12.0000, -5.0000, 16.0000],
                      [-12.0000, -10.0000, 12.0000],
                      [-12.0000, -10.0000, 0],
                      [-12.0000, -5.0000, 0],
                      [-12.0000, 0, 0],
                      [-12.0000, 0, 12.0000],
                      [-12.0000, 0, 0]])

    house = np.transpose(house)

    # add a vector of ones to the house matrix to represent the house in homogeneous coordinates
    house = np.vstack([house, np.ones(np.size(house, 1))])
    return house

cam, M_cam0 = init_cam()
house = init_obj()


'''for i in range(6):
    M_cam0 = x_rotation(180/4) @ M_cam0
    cam = x_rotation(180/4) @ cam
    MP = cam_projection(M_cam=M_cam0)
    proj = image_2d(MP=MP, obj=house)
    cam_view(proj)
    wolrd_view(house, cam)'''