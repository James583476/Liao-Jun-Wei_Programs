import pygame as pg

Run = 1
FPS = 60
DO_UPDATE = 20
NUM = 0
W,H = 1920//2, 1080//2
Gravity = [0, 9.8]
t = 0.5/FPS

pg.init()
screen = pg.display.set_mode((W,H))
clock = pg.time.Clock()

#def function
def vector_add(v,u):
    return [v[i]+u[i] for i in range(len(v))]

def vector_multiply(v,scalar):
    return [v[i]*scalar for i in range(len(v))]

def dot(v,u):
    return sum([v[i]*u[i] for i in range(len(v))])

def shadow_vector(v,u):#v在u上的投影向量
    if dot(u,u) == 0: return [0 for _ in range(len(v))]
    return vector_multiply(u,dot(v,u)/ dot(u,u))

def vector_length(v):
    return sum([v[i]**2 for i in range(len(v))])**0.5

class Point(pg.sprite.Sprite):
    def __init__(self,mass=1,x=0,y=0,radius=5,color=(255,255,255),move_enable=True):
        super().__init__()
        self.mass = mass
        self.X = [x+W//2,y+H//2,0,0,0,0]#(x,y,vx,vy,ax,ay)
        self.old_pos = self.X[:]
        self.rad = radius
        self.color = color
        self.move_enable = move_enable
    def draw(self,screen):
        pg.draw.circle(screen,self.color,self.X[:2],self.rad)

class Line(pg.sprite.Sprite):
    def __init__(self,point1,point2,color=(128,255,128),width=2):
        super().__init__()
        self.point1 = point1
        self.point2 = point2
        self.vector = [point2.X[0]-point1.X[0],point2.X[1]-point1.X[1]]#vector(p1p2)
        self.color = color
        self.width = width
        self.length = vector_length(self.vector)
        self.length_last = self.length
    def draw(self,screen):
        pg.draw.line(screen,self.color,self.point1.X[:2],self.point2.X[:2],width=self.width)
    def update(self):
        self.vector = [self.point2.X[0]-self.point1.X[0],self.point2.X[1]-self.point1.X[1]]
        self.length_last = vector_length(self.vector)

def update_1(self):
    if not self.move_enable: 
        self.X[5] = 0
        return
    self.X[0] += self.X[2]*t+0.5*self.X[4]*t**2
    self.X[1] += self.X[3]*t+0.5*self.X[5]*t**2
    self.X[2] += 0.5*self.X[4]*t
    self.X[3] += 0.5*self.X[5]*t

def update_2(self):
    if not self.move_enable: return
    self.X[2] += 0.5*self.X[4]*t
    self.X[3] += 0.5*self.X[5]*t

if __name__ == '__main__':
    points = pg.sprite.Group()
    point1 = Point(x=1,y=-150)
    point2 = Point(y=-100,move_enable=False)
    points.add(point1)
    points.add(point2)
    lines = pg.sprite.Group()
    line1 = Line(points.sprites()[0],points.sprites()[1])
    line1_length = line1.length
    lines.add(line1)

    while Run:
        for event in pg.event.get():
            if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                Run = 0
        screen.fill((0,0,0))

        #重力(update_1）
        for point in points:
            point.old_pos = point.X[:2].copy()
            point.X[4:6] = Gravity
            update_1(point)

        #修正位置
        for line in lines:
            line.update()
            delta = [line.point1.X[0] - line.point2.X[0],line.point1.X[1] - line.point2.X[1]]
            dist = vector_length(delta)
            if dist == 0:continue
            diff = (dist - line1_length) / dist
            w1 = 1 if point1.move_enable else 0
            w2 = 1 if point2.move_enable else 0
            w = w1 + w2
            correction = vector_multiply(delta,(1/w)*diff)
            if line.point1.move_enable:
                line.point1.X[0] -= correction[0]
                line.point1.X[1] -= correction[1]
            if line.point2.move_enable:
                line.point2.X[0] += correction[0]
                line.point2.X[1] += correction[1]
        #重新計算速度
        for point in points:
            v = vector_multiply(vector_add(point.X[:2],vector_multiply(point.old_pos,-1)),1/t)
            point.X[2:4] = v

        #update_2
        for point in points:
            update_2(point)
            line.draw(screen)
            point.draw(screen)
        
        pg.display.set_caption(f'{int(clock.get_fps())}')
        if NUM % DO_UPDATE == 0:
            clock.tick(FPS)
            pg.display.update()
        NUM += 1
pg.quit()
