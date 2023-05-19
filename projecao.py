from functions import *

from stl import mesh
import numpy as np



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



'''for i in range(6):
    M_cam0 = x_rotation(180/4) @ M_cam0
    cam = x_rotation(180/4) @ cam
    MP = cam_projection(M_cam=M_cam0)
    proj = image_2d(MP=MP, obj=house)
    cam_view(proj)
    wolrd_view(house, cam)'''