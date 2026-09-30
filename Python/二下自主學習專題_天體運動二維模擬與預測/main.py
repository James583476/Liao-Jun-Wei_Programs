import pygame as pg
import numpy as np
import tracker  #追蹤行為描述檔案
from math import pi,sin,cos
#from random import randrange

#位置更新使用歷程:
#   歐拉法->Velocity Verlet
#   力無法守恆->更改更新方法:
#       更新位置->更新一半速度->更新加速度->更新後半速度

pg.init()
BALL_NUM = 50
WIDTH = 1920/2
HIGH = 1080/2
COLOR = [[255,0,0],[255,128,0],[255,255,0],[255,255,127],[255,255,255],[127,255,127],[127,255,255],[127,127,255],[255,127,127],[255,0,255],
         [255,127,255],[127,127,127],[127,0,0],[127,63,0],[127,127,0],[127,127,63],[127,127,127],[63,127,63],[63,127,127],[63,63,127]]
RUN = 1
FPS = 120
AU = 1
SCALE = HIGH/5
SUN_M = 1.98847e30
G = 4*pi**2  #重力常數G     #由圓周-萬有引力推導，設R=1,M=1,T=1
t = tracker.t
screen = pg.display.set_mode((WIDTH,HIGH))
clock = pg.time.Clock()
USE_FIX_GRAVITY_EVENT = True

track_line = {}
print_track_line = True

class Ball(pg.sprite.Sprite):
    def __init__(self,x=0,y=0,vx=0.,vy=0.,ax=0.,ay=0.,radius=1.,weight=1/SUN_M,color=[255,255,255],move_enable = True):
        super().__init__()
        self.X = np.array([[x], [y], [vx], [vy], [ax], [ay]])    #(x,y,vx,vy,ax,ay)
        self.radius = radius
        self.weight = weight
        self.color = color
        rect_wh = self.radius*(2+2**0.5)/4
        x = self.X[0][0]*SCALE+WIDTH/2
        y = self.X[1][0]*SCALE+HIGH/2
        self.rect = pg.Rect(x-rect_wh,y-rect_wh,rect_wh*2,rect_wh*2)
        self.move_enable = move_enable
    def update_pos(self):
        if not self.move_enable:return
        #self.X = F @ self.X
        #位置更新->更新{半步}速度   **Velocity Verlet**
        self.X[0][0] += self.X[2][0]*t + 0.5*self.X[4][0]*t**2
        self.X[1][0] += self.X[3][0]*t + 0.5*self.X[5][0]*t**2
        self.X[2][0] += 0.5*self.X[4][0]*t#
        self.X[3][0] += 0.5*self.X[5][0]*t#
    def update_vel(self):
        if not self.move_enable: return
        #使用「新加速度」更新後半步速度 (v = v + 0.5*a_new*t)
        self.X[2][0] += 0.5*self.X[4][0]*t
        self.X[3][0] += 0.5*self.X[5][0]*t
        rect_wh = self.radius*(2+2**0.5)/4
        x = self.X[0][0]*SCALE+WIDTH/2
        y = self.X[1][0]*SCALE+HIGH/2
        self.rect.center = (x,y)

def display_Ball(ball):
    pg.draw.circle(screen,ball.color,ball.rect.center,ball.radius)
    #pg.draw.rect(screen,[255,0,0],ball.rect,width=1)

def gravity_event(balls):
    epsilon_sq = 0.01
    acceleration = [[0.,0.] for _ in range(len(balls))]
    for i in range(len(balls)):
        for j in range(i+1,len(balls)):
            distance = [balls[j].X[0] - balls[i].X[0],balls[j].X[1] - balls[i].X[1]]
            distance_non_direction = (distance[0]**2 + distance[1]**2+epsilon_sq)**0.5
            #if not distance_non_direction:continue #or distance_non_direction < 0.2
            a = (G*balls[j].weight/distance_non_direction**3)*distance
            acceleration[i][0] += a[0]
            acceleration[i][1] += a[1]
            acceleration[j][0] -= G * balls[i].weight * distance[0] / distance_non_direction**3
            acceleration[j][1] -= G * balls[i].weight * distance[1] / distance_non_direction**3
    return acceleration

def fix_gravity_event1(balls):  #fail
    epsilon_sq = 0.01
    acceleration = [[0.,0.] for _ in range(len(balls))]
    #total_pos = [0.,0.]
    #total_weight = 0
    total_pos = [sum(ball.X[0][0]*ball.weight for ball in balls), sum(ball.X[1][0]*ball.weight for ball in balls)]
    total_weight = sum(ball.weight for ball in balls)
    for i in range(len(balls)):
        others_pos = [total_pos[0] - balls[i].X[0]*balls[i].weight, total_pos[1] - balls[i].X[1]*balls[i].weight]
        others_pos[0] /= (total_weight - balls[i].weight)
        others_pos[1] /= (total_weight - balls[i].weight)
        others_weight = total_weight - balls[i].weight
        distance = [others_pos[0] - balls[i].X[0],others_pos[1] - balls[i].X[1]]
        distance_non_direction = (distance[0]**2 + distance[1]**2+epsilon_sq)**0.5
        a = (G*others_weight/distance_non_direction**3)*distance
        acceleration[i][0] += a[0]
        acceleration[i][1] += a[1]
    return acceleration

def fix_gravity_event(balls):
    epsilon = 0.01
    n = len(balls)

    pos = np.array([[b.X[0][0], b.X[1][0]] for b in balls])
    mass = np.array([b.weight for b in balls])

    # 正確方向：x_j - x_i
    dx = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]

    dist_sq = np.sum(dx**2, axis=2) + epsilon
    inv_dist3 = dist_sq ** (-1.5)

    # remove self-force
    mask = np.eye(n, dtype=bool)
    inv_dist3[mask] = 0
    dx[mask] = 0

    # j 對 i 的影響
    force = G * dx * inv_dist3[:, :, None] * mass[np.newaxis, :, None]

    acc = np.sum(force, axis=1)

    return acc.tolist()

def black_hole_mode(balls):
    balls.append(Ball(x=1,y=1,radius=25,weight=4000000,color=[150,2,0],move_enable=False))#銀河系中心人馬座A*約萬倍太陽質量
    #balls.append(Ball(x=0,y=0.5,radius=25,weight=4000000,color=[150,2,0],move_enable=False))#
    for i in range(1,BALL_NUM+1):
        balls.append(Ball(x=-3.5,y=(BALL_NUM/2-i)/3,vx=250,vy=-2500,weight=1000,radius=3,color=[255,255,255]))#COLOR[i-1]

def sun_earth_mode(balls):
    r = AU
    earth_m = 5.9722e24/SUN_M
    sun_m = 1
    v = (G*sun_m/r)**0.5
    balls.append(Ball(radius=20,weight=sun_m,color=[255,200,10],move_enable=False))
    balls.append(Ball(radius=5,weight=earth_m,x=-r,vy=-v,color=[100,100,255]))
    balls.append(Ball(x=-3.5,vx=0,vy=1))

def triple_ball_mode(balls):
    balls.append(Ball(y=-1,vx=1,radius=5,color=[255,127,127],weight=1))#
    balls.append(Ball(x=-0.5*3**0.5,y=0.5,vx=-0.5,vy=-0.5*3**0.5,radius=5,color=[127,255,127],weight=1))#
    balls.append(Ball(x=0.5*3**0.5,y=0.5,vx=-0.5,vy=0.5*3**0.5,radius=5,color=[127,127,255],weight=1))#

def multiple_ball_mode(balls):
    theta = 360/ BALL_NUM
    for i in range(BALL_NUM):
        x = 1 * cos((i+1) * theta)
        y = 1 * sin((i+1) * theta)
        balls.append(Ball(x=x,y=y,radius=3,weight=1000))

def show_track_line():
    for point_id, path in track_line.items():
        if len(path) < 2: continue
        
        points = []
        for p in path:
            px = p[0] * SCALE + WIDTH / 2
            py = p[1] * SCALE + HIGH / 2
            points.append((px, py))
        
        color = balls[point_id].color
        faded_color = [max(0, c - 100) for c in color] 
        pg.draw.lines(screen, faded_color, False, points, 1)

if __name__ == '__main__':
    balls = []
    balls_X_noise = {}
    black_hole_mode(balls)      #變更成此模式時需於tracker.py中更改t值(-> t =  1/(FPS*12*300))
    #sun_earth_mode(balls)      #變更成此模式時需於tracker.py中更改t值(-> t =  1/(FPS*12))
    #triple_ball_mode(balls)    #變更成此模式時需於tracker.py中更改t值(-> t =  1/(FPS*12))
    #multiple_ball_mode(balls)  #變更成此模式時需於tracker.py中更改t值(-> t =  1/(FPS*12*300))
    while RUN:
        screen.fill([0,0,0])
        for ball in balls:
            ball.update_pos()#
        acceleration = []
        if USE_FIX_GRAVITY_EVENT:
            acceleration = fix_gravity_event(balls)#
        else:
            acceleration = gravity_event(balls)#
        for i in range(len(balls)):
            balls[i].X[4][0] = acceleration[i][0]
            balls[i].X[5][0] = acceleration[i][1]
            balls[i].update_vel()#
        for i in range(len(balls)):
            balls_X_noise[i] = [balls[i].X[0][0], balls[i].X[1][0]]
            display_Ball(balls[i])
        track_line = tracker.main(balls_X_noise)
        if print_track_line:
            show_track_line()
        for event in pg.event.get():
            key = pg.key.get_pressed()
            if event.type == pg.QUIT or key[pg.K_ESCAPE]:
                RUN = 0
            if key[pg.K_F3]:    #顯示預測線與否
                print_track_line = not print_track_line
            if key[pg.K_F4]:    #切換重力模式
                USE_FIX_GRAVITY_EVENT = not USE_FIX_GRAVITY_EVENT
        pg.display.set_caption(f'Output\tfps:{int(clock.get_fps())}\tfast_mod:{USE_FIX_GRAVITY_EVENT}')#
        pg.display.update()
        clock.tick(FPS)
pg.quit()
