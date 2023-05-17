import pygame
from sys import exit
from matplotlib.backends.backend_agg import FigureCanvasAgg
from functions import *
from projecao import *

def draw_graphics(fig, h, mundo, w):
    renderer = fig.canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    surface = pygame.image.fromstring(raw_data, fig.canvas.get_width_height(), 'RGB')
    # Desenha a superfície com o gráfico
   # if mundo:
    #    view_world.blit(surface, surface.get_rect(bottomleft=(10, h)))
   # else:
    #    view_cam.blit(surface, surface.get_rect(bottomleft=(10, h)))
    screen.blit(surface, (w, h))
    fig.canvas.draw()
    #plt.show(block=False)

def display_cam_info(cam):
    # --- X, Y, Z Position
    position_surface = test_font.render(f'{cam[0,-1]: .1f}', False, "White")
    position_rect = position_surface.get_rect(midleft=(30, 40))
    cam_info_surface.blit(position_surface, position_rect)
    position_surface = test_font.render(f'{cam[1,-1]: .1f}', False, "White")
    position_rect = position_surface.get_rect(midleft=(30, 70))
    cam_info_surface.blit(position_surface, position_rect)
    position_surface = test_font.render(f'{cam[2,-1]: .1f}', False, "White")
    position_rect = position_surface.get_rect(midleft=(30, 100))
    cam_info_surface.blit(position_surface, position_rect)

    view_world.blit(cam_info_surface, (10, 10))


def display_warning():
    text_warning2 = test_font.render("X axis", False, 'Black')
    if Y:
        text_warning2 = test_font.render("Y axis", False, 'Black')
    elif Z:
        text_warning2 = test_font.render("Z axis", False, 'Black')
    text_warning_surface.blit(text_warning2, (text_warning.get_width()//2 -text_warning2.get_width()//2,
                                text_warning.get_height()+10))
    view_world.blit(text_warning_surface, (20, 150))
    #screen.blit(text_warning_surface, (20, height - h - 20))

def update_cam_translation(cam, M_cam0, ax_cam, ax_world):
    if referential_switch.is_on:
        if event.key == pygame.K_UP:
            cam = translate_cam_ref(dx, dy, dz, M_cam0) @ cam
            M_cam0 = translate_cam_ref(dx, dy, dz, M_cam0) @ M_cam0
        elif event.key == pygame.K_DOWN:
            cam = translate_cam_ref(-dx, -dy, -dz, M_cam0) @ cam
            M_cam0 = translate_cam_ref(-dx, -dy, -dz, M_cam0) @ M_cam0
    else:
        if event.key == pygame.K_UP:
            cam = translate(dx, dy, dz) @ cam
            M_cam0 = translate(dx, dy, dz) @ M_cam0
        elif event.key == pygame.K_DOWN:
            cam = translate(-dx, -dy, -dz) @ cam
            M_cam0 = translate(-dx, -dy, -dz) @ M_cam0

    MP = cam_projection(M_cam0, f)
    proj = image_2d(MP, obj)
    ax_world = world_view_frontend(fig_world, cam=cam, obj=obj)
    ax_cam = camera_view_frontend(fig_cam, proj)
    return cam, M_cam0, ax_cam, ax_world

def update_cam_rotation(cam, M_cam0, ax_cam, ax_world):
    if referential_switch.is_on:  # -- Camera
        if event.key == pygame.K_UP:
            cam = Rc @ cam
            M_cam0 = Rc @ M_cam0
        elif event.key == pygame.K_DOWN:
            cam = Rc_neg @ cam
            M_cam0 = Rc_neg @ M_cam0
    else:  # -- Mundo
        if event.key == pygame.K_UP:
            cam = Rw @ cam
            M_cam0 = Rw @ M_cam0
        elif event.key == pygame.K_DOWN:
            cam = Rw_neg @ cam
            M_cam0 = Rw_neg @ M_cam0

    MP = cam_projection(M_cam0, f)
    proj = image_2d(MP, obj)
    ax_world = world_view_frontend(fig_world, cam=cam, obj=obj)
    ax_cam = camera_view_frontend(fig_cam, proj)
    return cam, M_cam0, ax_cam, ax_world

pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Trabalho 1 - Visao Computacional")
clock = pygame.time.Clock()

view_world = pygame.Surface((width/2 - 20, height - 20))
view_world.fill('grey50')
view_cam = pygame.Surface((width/2 - 20, height - 20))
view_cam.fill('gray50')

test_font = pygame.font.Font(None, 30)
text_surface = test_font.render("Camera positiion", False, 'Green')
x_cam_surface = test_font.render("X: ", False, 'Green')
y_cam_surface = test_font.render("Y: ", False, 'Green')
z_cam_surface = test_font.render("Z: ", False, 'Green')

font = pygame.font.Font(None, 25)
text_warning = font.render("You are changing the", False, 'Black')

class SwitchButton:
    def __init__(self, x, y, width, height, on_color, off_color, textOFF='OFF', textON='ON', title='title'):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect2 = pygame.Rect(x+width, y, width, height)
        self.on_color = on_color
        self.off_color = off_color
        self.is_on = False

        self.font = pygame.font.Font(None, 20)
        self.fontT = pygame.font.Font(None, 25)
        self.text_surface = self.fontT.render(title, False, (20, 20, 20))
        self.buttonSurfaceOFF = pygame.Surface((width, height))
        self.buttonSurfOFF = self.font.render(textOFF, True, (20, 20, 20))
        self.text_rectOFF = self.buttonSurfOFF.get_rect(center=self.rect.center)
        #--
        self.buttonSurfaceON = pygame.Surface((width, height))
        self.buttonSurfON = self.font.render(textON, True, (20, 20, 20))
        self.text_rectON = self.buttonSurfON.get_rect(center=self.rect.center)

    def draw(self, surface):
        color_1 = self.on_color if self.is_on else self.off_color
        color_2 = self.off_color if self.is_on else self.on_color
        pygame.draw.rect(surface, color_1, self.rect,
                         border_top_left_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(surface, color_2, self.rect2,
                         border_top_right_radius=10,border_bottom_right_radius=10)
        surface.blit(self.text_surface, (self.rect.x, self.rect.y - self.rect.height // 2.5))
        surface.blit(self.buttonSurfOFF, (self.rect.x + self.rect.width // 2 - self.buttonSurfOFF.get_width() // 2,
                                       self.rect.y + self.rect.height // 2 - self.buttonSurfOFF.get_height() // 2))
        surface.blit(self.buttonSurfON, (self.rect2.x + self.rect2.width // 2 - self.buttonSurfON.get_width() // 2,
                                          self.rect2.y + self.rect2.height // 2 - self.buttonSurfON.get_height() // 2))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) or self.rect2.collidepoint(event.pos):
                self.is_on = not self.is_on

ON = (50, 50, 50)
OFF = (190, 190, 190)
print(view_cam.get_width())
referential_switch = SwitchButton(width - 230, 50, 100, 50, ON, OFF,
                                  textOFF="Camera", textON="World", title='Choose the Referential')
rot_tra_switch = SwitchButton(width//2 + 30, 50, 100, 50, ON, OFF,
                              textOFF="Rotation", textON="Translate", title="Choose Action")

cam, M_cam0 = init_cam()
f=50
sx=None
sy=None
angle, step=15, 1
obj = init_obj()

MP = cam_projection(M_cam0, f)
proj = image_2d(MP, obj)

# Criar a View do Mundo
fig_world = plt.figure(figsize=(6, 5))
ax_world = world_view_frontend(fig_world, cam=cam, obj=obj)
# Criar View da Camera
fig_cam = plt.figure(figsize=(6, 5))
ax_cam = camera_view_frontend(fig_cam, proj)

#
cam_info_surface = pygame.Surface((text_surface.get_width(), 120))
cam_info_surface.fill(color='gray50')
cam_info_surface.blit(text_surface, (0,0))
cam_info_surface.blit(x_cam_surface, (0,30))
cam_info_surface.blit(y_cam_surface, (0,60))
cam_info_surface.blit(z_cam_surface, (0,90))

text_warning_surface = pygame.Surface((text_warning.get_width(),text_warning.get_height()*2+20))
text_warning_surface.fill(color='white')
text_warning_surface.blit(text_warning, (0, 0))

# Converte o gráfico em uma superfície do Pygame
canvas = FigureCanvasAgg(fig_world)
w, h = canvas.get_width_height()
X, Y, Z = True, False, False
Rc, Rc_neg, Rw, Rw_neg = np.eye(4), np.eye(4), np.eye(4), np.eye(4)
dx, dy, dz = step, 0, 0

while True:
    screen.fill((20,20,20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                X, Y, Z = True, False, False
                dx, dy, dz = step, 0, 0
                Rw, Rc = x_rotation(angle), x_rotation_cam_ref(angle, M_cam0)
                Rw_neg, Rc_neg = x_rotation(-angle), x_rotation_cam_ref(-angle, M_cam0)
            elif event.key == pygame.K_y:
                X, Y, Z = False, True, False
                dx, dy, dz = 0, step, 0
                Rw, Rc = y_rotation(angle), y_rotation_cam_ref(angle, M_cam0)
                Rw_neg, Rc_neg = y_rotation(-angle), y_rotation_cam_ref(-angle, M_cam0)
            elif event.key == pygame.K_z:
                X, Y, Z = False, False, True
                dx, dy, dz = 0, 0, step
                Rw, Rc = z_rotation(angle), z_rotation_cam_ref(angle, M_cam0)
                Rw_neg, Rc_neg = z_rotation(-angle), z_rotation_cam_ref(-angle, M_cam0)
            if not(rot_tra_switch.is_on): ## --- Tranlacao
                cam, M_cam0, ax_cam, ax_world = update_cam_translation(cam, M_cam0, ax_cam, ax_world)
            if rot_tra_switch.is_on: # ---- Rotacao
                cam, M_cam0, ax_cam, ax_world = update_cam_rotation(cam, M_cam0, ax_cam, ax_world)
        referential_switch.update(event)
        rot_tra_switch.update(event)

    screen.blit(view_world, (10, 10))
    screen.blit(view_cam, (width / 2 + 10, 10))
    display_cam_info(cam)

    referential_switch.draw(screen)
    rot_tra_switch.draw(screen)

    # --- World
    #draw_graphics(fig_world, h=height-h-20, w=20, mundo=True)
    #draw_graphics(fig_world, h=int(height-h*0.14), mundo=True) #height-70
    display_warning()
    # --- Camera
    draw_graphics(fig_cam, h=height-h-20, w=width-w-20, mundo=False)
    #draw_graphics(fig_cam, h=int(height-h*0.14), mundo=False)

    print("-----------")
    print("-----------")
    print(cam)



    pygame.display.update()
    clock.tick(10)

# Limpa o arquivo temporário
import os
os.remove(temp_file)

