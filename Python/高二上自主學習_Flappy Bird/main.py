import pygame as pg
import os,random,datetime

W = 500       #288
H = 700       #512
FPS = 120
WHITE = (255,255,255)
GROUND_G = 50/FPS
BG_SPEED = 240/FPS
BIRD_TURN_ANGLE = 180/FPS 
FLOOR_HIGH = H/10
TUB_GAP_HIGH = 6
DO_PRINT_HIT_RECT = 0

pg.init()
window = pg.display.set_mode((W,H))
run = 1
clock = pg.time.Clock()
count = 0

class Bird(pg.sprite.Sprite):
    def __init__(self,w,h):
        super().__init__()
        self.x = W//10
        self.y = H//2
        f = (H + W) / 20
        self.fw = w*f/200
        self.fh = h*f/200
        self.ground_v = 0
        self.face_angle = 0.0
        underphoto = os.path.join('bird.png')
        underphoto = pg.image.load(underphoto).convert_alpha()
        surface = pg.Surface((w,h),pg.SRCALPHA,32)
        surface.blit(underphoto,(0,0),(0,0,w,h))
        self.sprited = pg.transform.scale(surface,(self.fw,self.fh))
        self.rect = self.sprited.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.sprite = pg.transform.rotate(self.sprited,self.face_angle)
        self.rect = self.sprite.get_rect(topleft = (self.x,self.y))
        self.rect = pg.rect.Rect(self.x,self.y,self.fw,self.fh)

    def draw(self,screen):
        screen.blit(self.sprite,(self.x,self.y))
        if DO_PRINT_HIT_RECT:
            pg.draw.rect(screen,(0,255,0),self.rect,2)

class BackGround(pg.sprite.Sprite):
    def __init__(self,w,h):
        self.h = H-FLOOR_HIGH + H//200 + 1
        self.w = w*(self.h)/h
        self.move_f = 0
        underphoto = os.path.join('背景.png')
        self.underphoto = pg.image.load(underphoto).convert_alpha()
        self.underphoto = pg.transform.scale(self.underphoto,(self.w,self.h))###
        self.surface = pg.Surface((W,self.h),pg.SRCALPHA,32)###
        self.surface.blit(self.underphoto,(0,0),(0,0,W,self.h))###
    
    def move(self):
        self.move_f += BG_SPEED
        self.surface.blit(self.underphoto,(0,0),(self.move_f,0,W,self.h))###
        if self.move_f >= self.w:   #self.w*(H-FLOOR_HIGH+1)/self.h
            self.move_f = 0
        elif self.move_f + W > self.w:  #self.w*(H-FLOOR_HIGH+1)/self.h
            self.surface.blit(self.underphoto,(self.w-self.move_f,0),(0,0,W,self.h))###
        self.sprite = pg.transform.scale(self.surface,(W,self.h))

    def draw(self,screen):
        screen.blit(self.sprite,(0,0))

class Ground(pg.sprite.Sprite):
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.floor_high = FLOOR_HIGH
        self.move_f = 0
        underground = os.path.join('floor.png')
        self.underground = pg.image.load(underground).convert_alpha()
        self.underground = pg.transform.scale(self.underground,(W,self.h/(self.w/W)))
        self.surface = pg.Surface((W,self.floor_high),pg.SRCALPHA,32)
        self.surface.blit(self.underground,(0,0),(0,0,w,h))

    def move(self):
        self.move_f += BG_SPEED
        if self.move_f >= W:
            self.move_f = 0
        self.surface.blit(self.underground,(W-self.move_f,0),(0,0,self.w,self.h))
        self.surface.blit(self.underground,(0,0),(self.move_f,0,self.w,self.h))
        self.sprite = pg.transform.scale(self.surface,(W,self.floor_high))
    def draw(self,screen):
        screen.blit(self.sprite,(0,H-self.floor_high))

class Tube(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.fw = int(bird.fw * 1.5)
        self.speed = BG_SPEED

        self.gap = int(bird.fh * TUB_GAP_HIGH)      # 洞的高度
        self.center_y = random.randint(int(self.gap),int(H - ground.floor_high ))#- self.gap

        self.x = W

        img = pg.image.load('水管.png').convert_alpha()
        img = pg.transform.scale(img, (self.fw, H))

        # 下水管
        bottom_h = H - self.center_y #- self.gap // 2
        self.bottom = img.subsurface((0, 0, self.fw, bottom_h))

        # 上水管（翻轉）
        top_h = self.center_y - self.gap #// 2
        self.top = img.subsurface((0, H - top_h, self.fw, top_h))
        #self.top = pg.transform.flip(img.subsurface((0, tube_total_high - top_h, self.fw, top_h)),False, True)
        self.bottom_rect = self.bottom.get_rect()
        self.top_rect = self.top.get_rect()

    def update(self):
        self.x -= self.speed
        self.bottom_rect.topleft = (self.x, H - ground.floor_high + 1 - self.bottom.get_height())
        self.top_rect.topleft = (self.x, 0)
        if self.x + self.fw < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.bottom, self.bottom_rect)
        screen.blit(self.top, self.top_rect)
        if DO_PRINT_HIT_RECT:
            pg.draw.rect(screen,(255,0,0),self.bottom_rect,2)
            pg.draw.rect(screen,(255,0,0),self.top_rect,2)

def move(actor,event):
    if event.key == pg.K_w or event.key == pg.K_SPACE or event.key == pg.K_UP:
        actor.ground_v = -8
        actor.face_angle = 45
    if event.key == pg.K_9:
        actor.face_angle += BIRD_TURN_ANGLE
    if event.key == pg.K_0:
        actor.face_angle -= BIRD_TURN_ANGLE
    if event.key == pg.K_t:
        actor.ground_v = 0
        actor.x = 60
        actor.y = H // 2
        actor.face_angle = 0
        background.move_f = ground.move_f = 0
    if event.key == pg.K_F3:
        global DO_PRINT_HIT_RECT
        if DO_PRINT_HIT_RECT:
            DO_PRINT_HIT_RECT = 0
        else:
            DO_PRINT_HIT_RECT = 1

def Menu_main(run):
    run_break = 0
    bird.update()
    while run_break == 0:
        clock.tick(FPS)
        background.move()
        ground.move()
        background.draw(window)
        ground.draw(window)
        bird.draw(window)
        for event in pg.event.get():
            key = pg.key.get_pressed()
            if event.type == pg.QUIT:
                run = 0
                run_break = 1
                break
            if key[pg.K_w] or key[pg.K_SPACE]:
                run_break = 1
                bird.ground_v = -8
                bird.face_angle = 45
                break
        pg.display.update()
    return run

def main(run,tube_print_time,count):
    while run:
        clock.tick(FPS)
        background.move()
        ground.move()
        background.draw(window)
        ground.draw(window)
        if bird.y < H-ground.floor_high - bird.fh:
            bird.ground_v += GROUND_G
            if bird.face_angle >-90:
                bird.face_angle -= BIRD_TURN_ANGLE
        else:
            bird.ground_v = 0
            bird.y = (H-ground.floor_high) - bird.fh
        bird.update()
        for event in pg.event.get():
            key = pg.key.get_pressed()
            if event.type == pg.QUIT or key[pg.K_ESCAPE]:
                run = 0
                break
            if event.type == pg.KEYDOWN:
                move(bird,event)
        bird.y += int(bird.ground_v)
        bird.draw(window)
        if tube_print_time % (W/BG_SPEED) == 0:
            tube_group.add(Tube())
        for sprite in tube_group:
            sprite.update()
            sprite.draw(window)
            if bird.rect.colliderect(sprite.bottom_rect) or bird.rect.colliderect(sprite.top_rect):
                run = 0
            if sprite.x == bird.x:
                count += 1
        pg.display.set_caption(f'Flappy Bird\tFPS = {int(clock.get_fps())}\tcount = {count}')
        pg.display.update()
        tube_print_time += 1
    pg.quit()
    return count

def Player_data_write(count):
    DataDate = datetime.datetime.now()
    with open("Player_data.txt","a",encoding="utf-8") as f:
        f.write(f"\"{DataDate}\"\tCount：{count}\n")

if __name__ == "__main__":
    bird = Bird(243,172)
    background = BackGround(900,504)
    ground = Ground(1479,481)
    tube_group = pg.sprite.Group()
    tube_print_time = 0
    run = Menu_main(run)
    count = main(run,tube_print_time,count)
    Player_data_write(count)
