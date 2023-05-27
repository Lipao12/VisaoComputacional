import tkinter as tk
from functions import *
import matplotlib.pyplot as plt
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None

def exibir_grafico():
    global canvas, cam, M_cam0, lbl_value_X, lbl_value_Y, lbl_value_Z, ax, ax2
    try:
        MP = cam_projection(M_cam0, f=f, cdd_h=cdd_h, cdd_w=cdd_w, width=width,height=height)
        proj = image_2d(MP, obj)

        ax.cla()
        ax = world_visualization(fig, ax=ax, cam=cam, obj=obj)
        ax2.cla()
        ax2 = camera_visualization(fig, proj, ax=ax2, width=width, height=height)

        canvas.draw()

        lbl_value_X.set(f'{cam[0, -1]: .1f}')
        lbl_value_Y.set(f'{cam[1, -1]: .1f}')
        lbl_value_Z.set(f'{cam[2, -1]: .1f}')
    except Exception as e:
        print("Error:", e)

def rotate_grafic(angle_x, angle_y, angle_z):
    global cam, M_cam0
    if not(camera):
        M = x_rotation(angle_x)@y_rotation(angle_y)@z_rotation(angle_z)
    else:
        M = x_rotation_cam_ref(angle_x, M_cam0)@y_rotation_cam_ref(angle_y, M_cam0)@z_rotation_cam_ref(angle_z, M_cam0)

    cam = M@cam
    M_cam0 = M@M_cam0
    exibir_grafico()

def move_grafic(step_x, step_y, step_z):
    global cam, M_cam0
    if not(camera):
        M = translate(step_x, step_y, step_z)
    else:
        M = translate_cam_ref(step_x, step_y, step_z, M_cam0)

    cam = M@cam
    M_cam0 = M@M_cam0
    exibir_grafico()

def move(step, axis):
    if axis == "X":
        move_grafic(step, 0, 0)
    elif axis == "Y":
        move_grafic(0, step, 0)
    elif axis == "Z":
        move_grafic(0, 0, step)

def rotate(angle, axis):
    if axis == "X":
        rotate_grafic(angle, 0, 0)
    elif axis == "Y":
        rotate_grafic(0, angle, 0)
    elif axis == "Z":
        rotate_grafic(0, 0, angle)

def camera_reference():
    global camera
    camera = not(camera)
    btn_cam_ref.configure(bg="#b9b9b9" if camera else initial_bg)
    btn_world_ref.configure(bg=initial_bg if camera else "#b9b9b9")

def change_values():
    global  f, cdd_w, cdd_h, MP, width, height
    try:
        f = float(f_input.get())
        cdd_w = float(cdd_w_input.get())
        cdd_h = float(cdd_h_input.get())
        width = float(width_input.get())
        height = float(height_input.get())
        exibir_grafico()

    except Exception as e:
        print("Error:", e)

def reset_cam_position():
    global cam, M_cam0
    cam, M_cam0 = init_cam()
    exibir_grafico()
def reset_values():
    global f, angle, step, cdd_w, cdd_h, height, width
    f = 50
    f_input.delete(0, tk.END)
    f_input.insert(0, f'{f}')
    angle = 15
    angle_input.delete(0, tk.END)
    angle_input.insert(0, f'{angle}')
    step = 5
    step_input.delete(0, tk.END)
    step_input.insert(0, f'{step}')
    cdd_w = 36
    cdd_w_input.delete(0, tk.END)
    cdd_w_input.insert(0, f'{cdd_w}')
    cdd_h = 24
    cdd_h_input.delete(0, tk.END)
    cdd_h_input.insert(0, f'{cdd_h}')
    width = 1280
    width_input.delete(0, tk.END)
    width_input.insert(0, f'{width}')
    height = 720
    height_input.delete(0, tk.END)
    height_input.insert(0, f'{height}')
    change_values()

def set_position():
    global cam, M_cam0
    x = float(set_x_input.get())
    y = float(set_y_input.get())
    z = float(set_z_input.get())
    cam, M_cam0 = set_cam_position(x, y, z, cam, M_cam0)
    exibir_grafico()

cam, M_cam0 = init_cam()
obj = translate(0,0,-9)@z_rotation(90)@init_obj()
angle = 15
step = 5
f = 50
width=1280
height=720
cdd_w = 36
cdd_h = 24
camera = False
MP = cam_projection(M_cam0, f)
proj = image_2d(MP, obj)
fig = plt.figure(figsize=(15, 5), dpi=100)#figsize=(6, 5))
ax = world_visualization(fig, cam=cam, obj=obj)
ax2 = camera_visualization(fig, proj)

window = tk.Tk()
window.title("Projeto 1 - Visão Computacional")
window.geometry("1500x709")
initial_bg = window.cget("bg")  # Cor de fundo padrão da janela

##
##
## Daqui para baixo é apenas criacao da interface
##
##

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)
title = tkFont.Font(size=11, weight="bold")

window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

button_frame1 = tk.Frame(window)
button_frame1.grid(row=0, column=0, padx=0, pady=2)
## --- Valores da Camera
lbl_value = tk.Label(master=button_frame1, text="Angle ")
lbl_value.grid(row=0, column=0, padx=2, pady=2)
angle_input = tk.Entry(button_frame1, textvariable=tk.StringVar(value=f'{angle}'))
angle_input.grid(row=0, column=1, pady=2)
lbl_value = tk.Label(master=button_frame1, text="Step ")
lbl_value.grid(row=1, column=0, padx=2, pady=2)
step_input = tk.Entry(button_frame1, textvariable=tk.StringVar(value=f'{step}'))
step_input.grid(row=1, column=1, pady=2)
lbl_value = tk.Label(master=button_frame1, text="Camera Intrinsic\nParam.", font=title)
lbl_value.grid(row=3, column=1, padx=2, pady=2)

button_frame2 = tk.Frame(button_frame1)
button_frame2.grid(row=4, column=1, padx=0, pady=2)
lbl_value = tk.Label(master=button_frame2, text="f ")
lbl_value.grid(row=0, column=0, padx=2, pady=2)
f_input = tk.Entry(button_frame2, width=5, textvariable=tk.StringVar(value=f'{f}'))
f_input.grid(row=0, column=1, pady=2, sticky="w")
lbl_value = tk.Label(master=button_frame2, text="cdd_w ")
lbl_value.grid(row=1, column=0, padx=2, pady=2)
cdd_w_input = tk.Entry(button_frame2, width=5,textvariable=tk.StringVar(value=f'{cdd_w}'))
cdd_w_input.grid(row=1, column=1, pady=2, sticky="w")
lbl_value = tk.Label(master=button_frame2, text="cdd_h ")
lbl_value.grid(row=2, column=0, padx=2, pady=2)
cdd_h_input = tk.Entry(button_frame2,width=5,textvariable=tk.StringVar(value=f'{cdd_h}'))
cdd_h_input.grid(row=2, column=1, pady=2, sticky="w")
lbl_value = tk.Label(master=button_frame2, text="width")
lbl_value.grid(row=0, column=3, padx=2, pady=2,sticky="w")
width_input = tk.Entry(button_frame2,width=7,textvariable=tk.StringVar(value=f'{width}'))
width_input.grid(row=0, column=4, pady=2)
lbl_value = tk.Label(master=button_frame2, text="heigth")
lbl_value.grid(row=1, column=3, padx=2, pady=2,sticky="w")
height_input = tk.Entry(button_frame2,width=7,textvariable=tk.StringVar(value=f'{height}'))
height_input.grid(row=1, column=4, pady=2)
#
bt_change = tk.Button(master=button_frame1, text="Change", command=change_values, width=10)
bt_change.grid(row=7, column=1, pady=2)

button_frame = tk.Frame(window)
button_frame.grid(row=0, column=1, padx=0, pady=2, sticky='w')

## --- Translation
lbl_value = tk.Label(master=button_frame, text="Translation", font=title)
lbl_value.grid(row=0, column=1)
lbl_value_X = tk.StringVar()
lbl_value_X.set(f'{cam[0,-1]: .1f}')
lbl_value = tk.Label(master=button_frame, text="X orientation")
lbl_value.grid(row=1, column=1)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: move(-float(step_input.get()), "X"), width=5)
btn_decreaseX.grid(row=2, column=0, padx=2)
lbl_value = tk.Label(master=button_frame, textvariable=lbl_value_X)
lbl_value.grid(row=2, column=1, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: move(float(step_input.get()), "X"), width=5)
btn_increaseX.grid(row=2, column=2, padx=2)

lbl_value_Y = tk.StringVar()
lbl_value_Y.set(f'{cam[1,-1]: .1f}')
lbl_value = tk.Label(master=button_frame, text="Y orientation")
lbl_value.grid(row=3, column=1)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: move(-float(step_input.get()), "Y"), width=5)
btn_decreaseX.grid(row=4, column=0, padx=2)
lbl_value = tk.Label(master=button_frame, textvariable=lbl_value_Y)
lbl_value.grid(row=4, column=1, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: move(float(step_input.get()), "Y"), width=5)
btn_increaseX.grid(row=4, column=2, padx=2)

lbl_value_Z = tk.StringVar()
lbl_value_Z.set(f'{cam[2,-1]: .1f}')
lbl_value = tk.Label(master=button_frame, text="Z orientation")
lbl_value.grid(row=5, column=1)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: move(-float(step_input.get()), "Z"), width=5)
btn_decreaseX.grid(row=6, column=0, padx=2)
lbl_value = tk.Label(master=button_frame, textvariable=lbl_value_Z)
lbl_value.grid(row=6, column=1, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: move(float(step_input.get()), "Z"), width=5)
btn_increaseX.grid(row=6, column=2, padx=2)

## --- Rotation
lbl_value = tk.Label(master=button_frame, text="Rotation", font=title)
lbl_value.grid(row=0, column=8)

lbl_value = tk.Label(master=button_frame, text="X orientation")
lbl_value.grid(row=1, column=8)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: rotate(-float(angle_input.get()), "X"), width=5)
btn_decreaseX.grid(row=2, column=7, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: rotate(float(angle_input.get()), "X"), width=5)
btn_increaseX.grid(row=2, column=9, padx=2)

lbl_value = tk.Label(master=button_frame, text="Y orientation")
lbl_value.grid(row=3, column=8)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: rotate(-float(angle_input.get()), "Y"), width=5)
btn_decreaseX.grid(row=4, column=7, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: rotate(float(angle_input.get()), "Y"), width=5)
btn_increaseX.grid(row=4, column=9, padx=2)

lbl_value = tk.Label(master=button_frame, text="Z orientation")
lbl_value.grid(row=5, column=8)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: rotate(-float(angle_input.get()), "Z"), width=5)
btn_decreaseX.grid(row=6, column=7, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: rotate(float(angle_input.get()), "Z"), width=5)
btn_increaseX.grid(row=6, column=9, padx=2)

lbl_value = tk.Label(master=button_frame, text="")
lbl_value.grid(row=0, column=10, padx=8)

## --- Definir a referencia
lbl_value = tk.Label(master=button_frame, text="Reference", font=title)
lbl_value.grid(row=0, column=12, padx=2)
btn_cam_ref = tk.Button(master=button_frame, text="Camera", command=camera_reference, width=10)
btn_cam_ref.grid(row=1, column=11, pady=2)
lbl_value = tk.Label(master=button_frame, text="")
lbl_value.grid(row=1, column=12)
btn_world_ref = tk.Button(master=button_frame, text="World", command=camera_reference, width=10, bg="#b9b9b9")
btn_world_ref.grid(row=1, column=13, pady=2)

set_pos_frame = tk.Frame(button_frame)
set_pos_frame.grid(row=3, column=11, pady=2)
lbl_value = tk.Label(master=set_pos_frame, text="x_pos")
lbl_value.grid(row=0, column=0, padx=2, pady=2,)
set_x_input = tk.Entry(set_pos_frame,width=7,textvariable=tk.StringVar(value=f'{cam[0,-1]}'))
set_x_input.grid(row=0, column=1, pady=2)
set_pos_frame = tk.Frame(button_frame)
set_pos_frame.grid(row=4, column=11, pady=2)
lbl_value = tk.Label(master=set_pos_frame, text="y_pos")
lbl_value.grid(row=0, column=0, padx=2, pady=2,)
set_y_input = tk.Entry(set_pos_frame,width=7,textvariable=tk.StringVar(value=f'{cam[1,-1]}'))
set_y_input.grid(row=0, column=1, pady=2)
set_pos_frame = tk.Frame(button_frame)
set_pos_frame.grid(row=5, column=11, pady=2)
lbl_value = tk.Label(master=set_pos_frame, text="z_pos")
lbl_value.grid(row=0, column=0, padx=2, pady=2,)
set_z_input = tk.Entry(set_pos_frame,width=7,textvariable=tk.StringVar(value=f'{cam[2,-1]}'))
set_z_input.grid(row=0, column=1, pady=2)
#
bt_change = tk.Button(master=button_frame, text="Set Position", command=set_position, width=10)
bt_change.grid(row=6, column=11, pady=2)

window.update()

button_frame2 = tk.Frame(window)
#button_frame2.place(x=(button_frame1.winfo_x()+button_frame.winfo_x())//2,
#                    y=0)
button_frame2.grid(row=0, column=0, pady=2, padx=30, sticky="e")
## --- Resetar parametros da camera
btn_resset_cam = tk.Button(master=button_frame2, text="Reset Camera\nParameters", command=reset_values, width=13)
btn_resset_cam.grid(row=1, column=2, pady=3)
btn_resset_cam_pos = tk.Button(master=button_frame2, text="Reset Camera\nPosition", command=reset_cam_position, width=13)
btn_resset_cam_pos.grid(row=2, column=2, pady=3)

# Inicie o loop principal do Tkinter
window.mainloop()