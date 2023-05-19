import tkinter as tk
from functions import *
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None

def exibir_grafico(dx, dy, dz):
    global canvas, cam, M_cam0, lbl_value_Y, lbl_value_Z, ax, ax2
    try:
        if not(camera):
            M = translate(dx, dy, dz)
        else:
            M = translate_cam_ref(dx, dy, dz, M_cam0)

        cam = M @ cam
        M_cam0 = M @ M_cam0

        MP = cam_projection(M_cam0, f=f, sx=sx, sy=sy)
        proj = image_2d(MP, obj)

        ax.cla()
        ax = world_view_frontend(fig, ax=ax, cam=cam, obj=obj)
        ax2.cla()
        ax2 = camera_view_frontend(fig, proj, ax=ax2)

        canvas.draw()

        lbl_value_X.set(f'{cam[0, -1]: .1f}')
        lbl_value_Y.set(f'{cam[1, -1]: .1f}')
        lbl_value_Z.set(f'{cam[2, -1]: .1f}')
    except Exception as e:
        print("Error:", e)

def rotate_grafico(angle_x, angle_y, angle_z):
    global cam, M_cam0
    if not(camera):
        M = x_rotation(angle_x)@y_rotation(angle_y)@z_rotation(angle_z)
    else:
        M = x_rotation_cam_ref(angle_x, M_cam0)@y_rotation_cam_ref(angle_y, M_cam0)@z_rotation_cam_ref(angle_z, M_cam0)

    cam = M@cam
    M_cam0 = M@M_cam0
    exibir_grafico(0,0,0)

def move(step, axis):
    if axis == "X":
        exibir_grafico(step, 0, 0)
    elif axis == "Y":
        exibir_grafico(0, step, 0)
    elif axis == "Z":
        exibir_grafico(0, 0, step)

def rotate(angle, axis):
    if axis == "X":
        rotate_grafico(angle, 0, 0)
    elif axis == "Y":
        rotate_grafico(0, angle, 0)
    elif axis == "Z":
        rotate_grafico(0, 0, angle)

def camera_reference():
    global camera
    camera = not(camera)
    btn_cam_ref.configure(bg="#b9b9b9" if camera else initial_bg)
    btn_world_ref.configure(bg=initial_bg if camera else "#b9b9b9")

def change_values():
    global  f, sx, sy, MP
    try:
        f = float(f_input.get())
        sx = float(sx_input.get())
        sy = float(sy_input.get())
        exibir_grafico(0, 0, 0)

    except Exception as e:
        print("Error:", e)

def reset_cam_position():
    global cam, M_cam0
    cam, M_cam0 = init_cam()
    exibir_grafico(0,0,0)
def reset_values():
    global f, angle, step, sx, sy
    f = 50
    f_input.delete(0, tk.END)
    f_input.insert(0, f'{f}')
    angle = 15
    angle_input.delete(0, tk.END)
    angle_input.insert(0, f'{angle}')
    step = 5
    step_input.delete(0, tk.END)
    step_input.insert(0, f'{step}')
    sx = None
    sx_input.delete(0, tk.END)
    sx_input.insert(0, f'{35}')
    sy = None
    sy_input.delete(0, tk.END)
    sy_input.insert(0, f'{30}')
    change_values()

window = tk.Tk()
window.title("Projeto 1 - Visão Computacional")
window.geometry("1500x709")

cam, M_cam0 = init_cam()
obj = translate(0,0,-9)@z_rotation(90)@init_obj2()
f = 50
angle = 15
step = 5
sx = None
sy = None
camera = False
MP = cam_projection(M_cam0, f)
proj = image_2d(MP, obj)
fig = plt.figure(figsize=(15, 5), dpi=100)#figsize=(6, 5))
ax = world_view_frontend(fig, cam=cam, obj=obj)
ax2 = camera_view_frontend(fig, proj)
initial_bg = window.cget("bg")  # Cor de fundo padrão da janela

# Crie um canvas do Tkinter para exibir o gráfico inicial
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

button_frame = tk.Frame(window)
button_frame.grid(row=0, column=0, padx=0, pady=2)
## --- Valores da Camera
lbl_value = tk.Label(master=button_frame, text="Camera Values")
lbl_value.grid(row=0, column=1, padx=2, pady=2)
lbl_value = tk.Label(master=button_frame, text="Angle ")
lbl_value.grid(row=1, column=0, padx=2, pady=2)
angle_input = tk.Entry(button_frame, textvariable=tk.StringVar(value=f'{angle}'))
angle_input.grid(row=1, column=1, pady=2)
lbl_value = tk.Label(master=button_frame, text="Step ")
lbl_value.grid(row=2, column=0, padx=2, pady=2)
step_input = tk.Entry(button_frame, textvariable=tk.StringVar(value=f'{step}'))
step_input.grid(row=2, column=1, pady=2)
lbl_value = tk.Label(master=button_frame, text="")
lbl_value.grid(row=3, column=0, padx=2, pady=2)
lbl_value = tk.Label(master=button_frame, text="f ")
lbl_value.grid(row=4, column=0, padx=2, pady=2)
f_input = tk.Entry(button_frame, textvariable=tk.StringVar(value=f'{f}'))
f_input.grid(row=4, column=1, pady=2)
lbl_value = tk.Label(master=button_frame, text="sx ")
lbl_value.grid(row=5, column=0, padx=2, pady=2)
sx_input = tk.Entry(button_frame, textvariable=tk.StringVar(value='35'))
sx_input.grid(row=5, column=1, pady=2)
lbl_value = tk.Label(master=button_frame, text="sy ")
lbl_value.grid(row=6, column=0, padx=2, pady=2)
sy_input = tk.Entry(button_frame, textvariable=tk.StringVar(value='30'))
sy_input.grid(row=6, column=1, pady=2)
#
bt_change = tk.Button(master=button_frame, text="Change", command=change_values, width=10)
bt_change.grid(row=7, column=1, pady=2)
window.update()

button_frame1 = tk.Frame(window)
button_frame1.place(x=button_frame.winfo_x() + button_frame.winfo_width(),
                    y=0)
## --- Resetar parametros da camera
btn_resset_cam = tk.Button(master=button_frame1, text="Reset Cam Parameters", command=reset_values, width=int(window.winfo_width()*0.013), height=int(window.winfo_y()*0.025))
btn_resset_cam.grid(row=0, column=0, pady=3)
btn_resset_cam_pos = tk.Button(master=button_frame1, text="Reset Cam Position", command=reset_cam_position, width=int(window.winfo_width()*0.013), height=int(window.winfo_y()*0.025))
btn_resset_cam_pos.grid(row=1, column=0, pady=3)

button_frame = tk.Frame(window)
button_frame.grid(row=0, column=1, padx=0, pady=2)
## --- Definir a referencia
lbl_value = tk.Label(master=button_frame, text="Reference")
lbl_value.grid(row=0, column=7, padx=2)
btn_cam_ref = tk.Button(master=button_frame, text="Camera", command=camera_reference, width=10)
btn_cam_ref.grid(row=1, column=6, pady=2)
lbl_value = tk.Label(master=button_frame, text="")
lbl_value.grid(row=1, column=7)
btn_world_ref = tk.Button(master=button_frame, text="World", command=camera_reference, width=10, bg="#b9b9b9")
btn_world_ref.grid(row=1, column=8, pady=2)

## --- Translation
lbl_value = tk.Label(master=button_frame, text="Translation")
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
lbl_value = tk.Label(master=button_frame, text="Rotation")
lbl_value.grid(row=0, column=12)

lbl_value = tk.Label(master=button_frame, text="X orientation")
lbl_value.grid(row=1, column=12)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: rotate(-float(angle_input.get()), "X"), width=5)
btn_decreaseX.grid(row=2, column=11, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: rotate(float(angle_input.get()), "X"), width=5)
btn_increaseX.grid(row=2, column=13, padx=2)

lbl_value = tk.Label(master=button_frame, text="Y orientation")
lbl_value.grid(row=3, column=12)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: rotate(-float(angle_input.get()), "Y"), width=5)
btn_decreaseX.grid(row=4, column=11, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: rotate(float(angle_input.get()), "Y"), width=5)
btn_increaseX.grid(row=4, column=13, padx=2)

lbl_value = tk.Label(master=button_frame, text="Z orientation")
lbl_value.grid(row=5, column=12)
btn_decreaseX = tk.Button(master=button_frame, text="-", command=lambda: rotate(-float(angle_input.get()), "Z"), width=5)
btn_decreaseX.grid(row=6, column=11, padx=2)
btn_increaseX = tk.Button(master=button_frame, text="+", command=lambda: rotate(float(angle_input.get()), "Z"), width=5)
btn_increaseX.grid(row=6, column=13, padx=2)

# Inicie o loop principal do Tkinter
window.mainloop()