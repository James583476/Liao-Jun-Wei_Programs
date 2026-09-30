import pygame as pg
import numpy as np

pg.init()
FPS = 60
near = 0.1
far = 100
C_eye = np.array([-0.3,4.,8.])
C_direction = np.array([0.,0.,-1.])#
Vx = np.array([1.,0.,0.])#
Vy = np.array([0.,1.,0.])#
C_up = np.array([0.,1.,0.])
FOV = 60
H = int(1080 / 2)
W = int(1920 / 2)
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
Run = 1

old_mouse_pos = None

class Point:
    def __init__(self,x,y,z,color=(255,255,255)):
        self.pos = np.array([[x],[y],[z],[1]])
        self.pos_after = np.array([[0.],[0.],[0.]])
        self.color = color
    def draw(self,screen):
        screen_x = int(self.pos_after[0][0]*(W/2) + W/2)
        screen_y = int(-self.pos_after[1][0]*(H/2) + H/2)
        pg.draw.circle(screen,self.color,(screen_x,screen_y),4)

def model_matrix(translate=np.array([0,0,0]),scale=np.array([1,1,1]),rotate=np.array([0,0,0])):  
    rad = rotate
    #rad = rotate * np.pi/180   #rotate使用角度制
    Ss = np.array([[scale[0],0,0,0],
                  [0,scale[1],0,0],
                  [0,0,scale[2],0],
                  [0,0,0,1]])
    Rx = np.array([[1,0,0,0],
                   [0,np.cos(rad[0]),-np.sin(rad[0]),0],
                   [0,np.sin(rad[0]),np.cos(rad[0]),0],
                   [0,0,0,1]])
    Ry = np.array([[np.cos(rad[1]),0,np.sin(rad[1]),0],
                   [0,1,0,0],
                   [-np.sin(rad[1]),0,np.cos(rad[1]),0],
                   [0,0,0,1]])
    Rz = np.array([[np.cos(rad[2]),-np.sin(rad[2]),0,0],
                   [np.sin(rad[2]),np.cos(rad[2]),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
    Tt = np.array([[1, 0, 0, translate[0]],
                  [0, 1, 0, translate[1]],
                  [0, 0, 1, translate[2]],
                  [0, 0, 0, 1]])
    return Tt @ Rz @ Ry @ Rx @ Ss   #往後固定使用此順序!!

def view_matrix(eye=C_eye,vec=C_direction,up=C_up):
    Vz = -vec/np.linalg.norm(vec)    # norm:範數 三維空間代表向量幾何長度
    Vx = np.cross(up,Vz)/np.linalg.norm(np.cross(up,Vz))    # 費羅貝尼烏斯範數 (Frobenius Norm)，通常用於衡量一個矩陣的「大小」或「長度」
    Vy = np.cross(Vz,Vx)/np.linalg.norm(np.cross(Vz,Vx))
    M = np.array([[Vx[0],Vx[1],Vx[2],-np.dot(Vx,eye)],
                  [Vy[0],Vy[1],Vy[2],-np.dot(Vy,eye)],
                  [Vz[0],Vz[1],Vz[2],-np.dot(Vz,eye)],
                  [0,0,0,1]])
    return M,Vx,Vy

def projection_matrix(near,far,fov_y=FOV,aspect=W/H):  #fov_y視野大小(使用角度制)
    fov_rad = fov_y * np.pi/180
    t = near * np.tan(fov_rad/2)
    r = t * aspect
    Pp = np.array([[near/r,0,0,0],
                   [0,near/t,0,0],
                   [0,0,-(far+near)/(far-near),-2*far*near/(far-near)],
                   [0,0,-1,0]])
    return Pp

def update_points(points,matrix):
    for point in points:
        pos = matrix @ point.pos
        if pos[3][0] <= 1e-8:
            continue
        point.pos_after[0][0] = pos[0][0]/pos[3][0]
        point.pos_after[1][0] = pos[1][0]/pos[3][0]
        point.pos_after[2][0] = pos[2][0]/pos[3][0]

def draw_edges(points, screen):
    edges = [
        (0,1), (1,2), (2,3), (3,0), # 下底面
        (4,5), (5,6), (6,7), (7,4), # 上頂面
        (0,4), (1,5), (2,6), (3,7)  # 垂直柱
    ]

    proj = []
    for p in points:
        x = int(p.pos_after[0][0]*(W/2) + W/2)
        y = int(-p.pos_after[1][0]*(H/2) + H/2)
        proj.append((x,y))

    for e in edges:
        if e == (3,0): 
            pg.draw.line(screen, (255,0,0), proj[e[0]], proj[e[1]], 2)
        elif e == (3,7): 
            pg.draw.line(screen, (0,0,255), proj[e[0]], proj[e[1]], 2)
        elif e == (2,3): 
            pg.draw.line(screen, (0,255,0), proj[e[0]], proj[e[1]], 2)
        else:
            pg.draw.line(screen, (255,255,255), proj[e[0]], proj[e[1]], 2)

def mov(key):
    global C_eye,C_direction,C_up,FOV
    speed = 0.1
    view_vec = speed * C_direction
    view_forward = [view_vec[0],0.,view_vec[2]]
    view_forward = view_forward/np.linalg.norm(view_forward)*speed
    view_right = np.cross(view_vec,C_up)/np.linalg.norm(np.cross(view_vec,C_up))*speed
    if key[pg.K_w]:
        C_eye += view_forward
    if key[pg.K_s]:
        C_eye -= view_forward
    if key[pg.K_a]:
        C_eye -= view_right
    if key[pg.K_d]:
        C_eye += view_right
    if key[pg.K_z]:
        C_eye[1] -= speed
    if key[pg.K_SPACE]:
        C_eye[1] += speed
    if key[pg.K_UP]:
        C_eye += view_vec
    if key[pg.K_DOWN]:
        C_eye -= view_vec
    if key[pg.K_RIGHT] and FOV < 179:
        FOV += 1
    if key[pg.K_LEFT] and FOV > 1:
        FOV -= 1

def mouse_mov(old_pos,Vx,Vy):
    key = pg.mouse.get_pressed()
    vec_out = [0.,0.,0.]
    if key[0]:
        global W,H
        pos = np.array([pg.mouse.get_pos()[0] - W/2,H/2 - pg.mouse.get_pos()[1]])
        if old_pos is not None:
            move = pos - old_pos
            move = np.array([[move[0]],[move[1]]])    #screen_pos
            F_mat = np.array([[Vx[0],Vy[0]],
                              [Vx[1],Vy[1]],
                              [Vx[2],Vy[2]]])
            vec = F_mat @ move
            sens = 0.01
            vec_out = np.array([vec[0][0]*sens,vec[1][0]*sens,vec[2][0]*sens])
        return pos, vec_out
    else:
        return None, vec_out

if __name__ == "__main__":
    points = [
        # === 下底面 (Y = -2) ===
        Point(2, -2, -2, (25, 25, 25)),     # 0
        Point( 2, -2, 2, (255, 0, 0)),      # 1
        Point(-2, -2,  2, (0, 255, 0)),     # 2
        Point(-2, -2, -2, (0, 0, 255)),     # 3
        # === 上頂面 (Y = 2) ===
        Point( 2,  2, -2, (255, 255, 0)),   # 4
        Point( 2,  2,  2, (255, 0, 255)),   # 5
        Point(-2,  2,  2, (0, 255, 255)),   # 6
        Point(-2,  2, -2, (255, 255, 255))  # 7
    ]

    while Run:
        clock.tick(FPS)
        screen.fill((0,0,0))
        old_mouse_pos,V_vec = mouse_mov(old_mouse_pos,Vx,Vy)
        d_camera_view = C_direction + V_vec                       #
        d_camera_view = d_camera_view/np.linalg.norm(d_camera_view)   #
        if np.dot(d_camera_view,C_up) > 0.99:   #避免攝影機翻轉
            d_camera_view = C_direction
        else:
            C_direction = d_camera_view
        V,Vx,Vy = view_matrix(eye=C_eye,vec=C_direction,up=C_up)
        M = model_matrix()
        P = projection_matrix(near,far,FOV,W/H)
        PVM = P @ V @ M
        update_points(points,PVM)
        draw_edges(points, screen)#
        for p in points:
            p.draw(screen)##
        key = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT or key[pg.K_ESCAPE]:
                Run = 0
        mov(key)
        pg.display.set_caption(f'FPS {int(clock.get_fps())}\tEye: {C_eye}\tFOV: {FOV}')#
        pg.display.update()
pg.quit()
