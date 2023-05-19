import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import pi, cos, sin

### Setting printing options
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
np.set_printoptions(precision=3, suppress=True)

def d2rad(angle):
    return (angle * pi)/180

def rad2d(angle):
    return (angle * 180)/pi

def translate(dx, dy, dz):
    T = np.eye(4)
    T[0, -1] = dx
    T[1, -1] = dy
    T[2, -1] = dz
    return T

def z_rotation(angle):
    angle = d2rad(angle)
    rotation_matrix = np.array(
        [[cos(angle), -sin(angle), 0, 0], [sin(angle), cos(angle), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return rotation_matrix


def x_rotation(angle):
    angle = d2rad(angle)
    rotation_matrix = np.array(
        [[1, 0, 0, 0], [0, cos(angle), -sin(angle), 0], [0, sin(angle), cos(angle), 0], [0, 0, 0, 1]])
    return rotation_matrix


def y_rotation(angle):
    angle = d2rad(angle)
    rotation_matrix = np.array(
        [[cos(angle), 0, sin(angle), 0], [0, 1, 0, 0], [-sin(angle), 0, cos(angle), 0], [0, 0, 0, 1]])
    return rotation_matrix


def set_plot(ax=None, figure=None, lim=[-2, 2]):
    if figure == None:
        figure = plt.figure(figsize=(8, 8))
    if ax == None:
        ax = plt.axes(projection='3d')

    ax.set_title("camera referecnce")
    ax.set_xlim(lim)
    ax.set_xlabel("x axis")
    ax.set_ylim(lim)
    ax.set_ylabel("y axis")
    ax.set_zlim(lim)
    ax.set_zlabel("z axis")
    return ax


# adding quivers to the plot
def draw_arrows(point, base, axis, length=1.5):
    # The object base is a matrix, where each column represents the vector
    # of one of the axis, written in homogeneous coordinates (ax,ay,az,0)

    # Plot vector of x-axis
    axis.quiver(point[0], point[1], point[2], base[0, 0], base[1, 0], base[2, 0], color='red', pivot='tail',
                length=length)
    # Plot vector of y-axis
    axis.quiver(point[0], point[1], point[2], base[0, 1], base[1, 1], base[2, 1], color='green', pivot='tail',
                length=length)
    # Plot vector of z-axis
    axis.quiver(point[0], point[1], point[2], base[0, 2], base[1, 2], base[2, 2], color='blue', pivot='tail',
                length=length)

    return axis

def world_view(obj, cam):
    ax0 = set_plot(lim=[-20, 40])
    draw_arrows(cam[:, -1], cam[:, 0:-1], ax0)
    ax0.plot3D(obj[0, :], obj[1, :], obj[2, :], 'red')
    # Plotando a quina da casa que está em (0,0,0) para servir de referência
    ax0.scatter(obj[0, 0], obj[1, 0], obj[2, 0], 'b')
    # Plote a câmera também - adicione o código abaixo

    draw_arrows(cam[:, -1], cam[:, 0:3], ax0)

    plt.show()

def world_view_frontend(fig=None, cam=None, obj=None):
    ax = fig.add_subplot(121, projection='3d')
    lim = [-20, 20]
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_zlim(lim)

    draw_arrows(cam[:, -1], cam[:, 0:-1], ax)
    ax.plot3D(obj[0, :], obj[1, :], obj[2, :], 'red')
    # Plotando a quina da casa que está em (0,0,0) para servir de referência
    ax.scatter(obj[0, 0], obj[1, 0], obj[2, 0], 'b')
    # Plote a câmera também - adicione o código abaixo
    draw_arrows(cam[:, -1], cam[:, 0:3], ax)

    return ax


###################################################################
############################  Camera  #############################
###################################################################

def translate_cam_ref(dx, dy, dz, M):
    T = np.eye(4)
    T[0, -1] = dx
    T[1, -1] = dy
    T[2, -1] = dz
    return M @ T @ np.linalg.inv(M)

def z_rotation_cam_ref(angle, M):
    angle = d2rad(angle)
    rotation_matrix = np.array([[cos(angle), -sin(angle), 0, 0],
                                [sin(angle), cos(angle), 0, 0],
                                [0, 0, 1, 0], [0, 0, 0, 1]])
    return M @ rotation_matrix @ np.linalg.inv(M)


def x_rotation_cam_ref(angle, M):
    angle = d2rad(angle)
    rotation_matrix = np.array([[1, 0, 0, 0], [0, cos(angle), -sin(angle), 0],
                                [0, sin(angle), cos(angle), 0],
                                [0, 0, 0, 1]])
    return M @ rotation_matrix @ np.linalg.inv(M)


def y_rotation_cam_ref(angle, M):
    angle = d2rad(angle)
    rotation_matrix = np.array([[cos(angle), 0, sin(angle), 0],
                                [0, 1, 0, 0], [-sin(angle), 0, cos(angle), 0],
                                [0, 0, 0, 1]])
    return M @ rotation_matrix @ np.linalg.inv(M)

def cam_projection(M_cam, f, cdd_w=36, cdd_h=24, s0=0, width=1280, height=720, sx=None, sy=None):
    if sx==None:
        sx = width / cdd_w
    if sy==None:
        sy = height / cdd_h
    Ox = width / 2
    Oy = height / 2
    K = np.array([[f*sx, f*s0, Ox],
                  [0, f*sy, Oy],
                  [0, 0, 1],])
    canon = np.hstack((np.eye(3),np.zeros((3,1))))
    g = np.linalg.inv(M_cam)

    return K @ canon @ g

def image_2d(MP, obj):
    proj = MP @ obj
    proj[0, :] = proj[0, :] / proj[2, :]
    proj[1, :] = proj[1, :] / proj[2, :]
    return proj

def set_cam_position(dx, dy, dz, cam, M):
    cam[:, -1] = dx, dy, dz, 1
    M[:, -1] = dx, dy, dz, 1
    return cam, M

def cam_view(proj, width=1280, height=720):
    # Plota a imagem
    #fig = plt.figure()
    ax1 = plt.axes()
    ax1.set_title("Imagem")
    # Acerte os limites do eixo X
    ax1.set_xlim([0, width])
    # Acerte os limites do eixo Y
    # Para inverter, basta colocar o valor máximo primeiro e o valor mínimo depois
    ax1.set_ylim([height, 0])  # (max, min) -- isso faz com que o y fique da forma usual na imagem

    plt.plot(proj[0, :], proj[1, :])

    ax1.plot(3, 4)
    ax1.grid('True')
    ax1.set_aspect('equal')

    plt.show()


def camera_view_frontend(fig, proj, width=1280, height=720):
    ax = fig.add_subplot(122)
    #ax = plt.axes()
    ax.set_title("Imagem")
    ax.set_xlim([0, width])
    ax.set_ylim([height, 0])

    plt.plot(proj[0, :], proj[1, :])

    ax.grid('True')
    ax.set_aspect('equal')
    return ax