import pygame
import math
import os
import sys
import random
import sqlite3
import time

pygame.init()
RUNNING = True
carpx = 150
carpos = 550
scorepx = 40
speed = 15
ylturn = False
rlturn = False
gap = 180
inc=1
counter = -gap
height = 800
os.environ['SDL_VIDEO_CENTERED'] = "0"
clock = pygame.time.Clock()
way = random.randint(0, 1)
ch = random.randint(0, 1)
gameover = False
ScoreArr = [None]*16
yx = 125 + math.floor((125-carpx)/2)
yy = carpos
rx = 250 + math.floor((125-carpx)/2)
ry = carpos
score = 0
best = 0
start = True
stng = False
YKEY = 100
RKEY = 107
begin = False
go = 0
name = ''
info = False
paused = False
timer = False

raleway_30 = pygame.font.Font('Orbitron-Medium.ttf',40)
raleway_20 = pygame.font.Font('Orbitron-Regular.ttf',25)
raleway = pygame.font.Font('Orbitron-Black.ttf',60)
raleway_15 = pygame.font.Font('Orbitron-Regular.ttf',20)

conn = sqlite3.connect('twocar.db')
c = conn.cursor()
try:
    print('try running')
    c.execute("""
        SELECT * FROM detail
    """)
    detail = c.fetchall()
    if len(detail) > 0:
        name = detail[0][0]
        best = detail[0][1]
        RKEY = detail[0][2]
        YKEY = detail[0][3]


except Exception:
    print('catch running')
    begin = True

if begin:
    c.execute("""CREATE TABLE detail (
        name text,
        score integer,
        rkey integer,
        ykey integer
            )""")

class Point(object):
    track = None
    yydist = None
    yxdist = None
    rxdist = None

    def __init__(self, trck, pos):

        self.point = pygame.transform.scale(
            pygame.image.load('point.png'), (scorepx, scorepx))
        self.pointPos = pos
        self.track = trck

    def move(self):
        global score
        global gameover
        # print(self.track,self.pointPos)

        if self.pointPos >= carpos + 125:
            gameover = True
            # return True

        if not gameover and not paused:
            self.pointPos += speed
        screen.blit(
            self.point, (((self.track*125)+math.floor((125-scorepx)/2)), self.pointPos))
        self.yydist = yy - self.pointPos
        if self.yydist <= 14 and self.yydist >= -116:
            yxdist = ((self.track*125)+math.floor((125-scorepx)/2))-yx
            rxdist = ((self.track*125)+math.floor((125-scorepx)/2))-rx
            if self.track == 0:
                if yxdist <= 55 and yxdist >= 3:
                    score += 1
                    return True
            elif self.track == 1:
                if yxdist >= 54 and yxdist <= 105:
                    score += 1
                    return True
            elif self.track == 2:
                if rxdist <= 55 and rxdist >= 3:
                    score += 1
                    return True
            elif self.track == 3:
                if rxdist >= 54 and rxdist <= 105:
                    score += 1
                    return True


class Virus(object):
    track = None
    yydist = None
    yxdist = None

    def __init__(self, trck, pos):
        # print(trck,pos)
        self.virus = pygame.transform.scale(
            pygame.image.load('virus.png'), (scorepx, scorepx))
        self.virusPos = pos
        self.track = trck

    def move(self):
        global gameover
        if self.virusPos >= height:
            return True
        if not gameover and not paused:
            self.virusPos += speed
        screen.blit(
            self.virus, (((self.track*125)+math.floor((125-scorepx)/2)), self.virusPos))

        self.yydist = yy-self.virusPos
        if self.yydist <= 14 and self.yydist >= -116:
            yxdist = ((self.track*125)+math.floor((125-scorepx)/2))-yx
            rxdist = ((self.track*125)+math.floor((125-scorepx)/2))-rx
            if self.track == 0:
                if yxdist <= 55 and yxdist >= 3:
                    gameover = True
                    # return True
            elif self.track == 1:
                # print (yxdist)
                if yxdist >= 54 and yxdist <= 105:
                    gameover = True
                    # return True
            elif self.track == 2:
                if rxdist <= 55 and rxdist >= 3:
                    gameover = True
            elif self.track == 3:
                if rxdist >= 54 and rxdist <= 105:
                    gameover = True


screen = pygame.display.set_mode((500, height))

ycar = [pygame.transform.scale(pygame.image.load('ycar.png'), (150, 150)),
        pygame.transform.scale(pygame.image.load('ycar10.png'), (132, 132)),
        pygame.transform.scale(pygame.image.load('ycar20.png'), (120, 120))]

ycar1 = [pygame.transform.scale(pygame.image.load('ycar.png'), (150, 150)),
         pygame.transform.scale(pygame.image.load('ycarm10.png'), (132, 132)),
         pygame.transform.scale(pygame.image.load('ycarm20.png'), (120, 120))]

rcar = [pygame.transform.scale(pygame.image.load('rcar.png'), (150, 150)),
        pygame.transform.scale(pygame.image.load('rcarm10.png'), (132, 132)),
        pygame.transform.scale(pygame.image.load('rcarm20.png'), (120, 120))]

rcar1 = [pygame.transform.scale(pygame.image.load('rcar.png'), (150, 150)),
         pygame.transform.scale(pygame.image.load('rcar10.png'), (132, 132)),
         pygame.transform.scale(pygame.image.load('rcar20.png'), (120, 120))]

settings = pygame.transform.scale(pygame.image.load('cogwheel.png'), (64, 64))
restart = pygame.transform.scale(pygame.image.load('reset.png'), (64, 64))
play = pygame.transform.scale(pygame.image.load('play-button.png'), (64, 64))
back = pygame.transform.scale(pygame.image.load('return.png'), (64, 64))
c1 = pygame.transform.scale(pygame.image.load('circle-outline.png'), (200, 200))
c2 = pygame.transform.scale(pygame.image.load('circle-outline1.png'), (200, 200))
jstick = pygame.transform.scale(pygame.image.load('joystick.png'),(100,100))
fw = pygame.transform.scale(pygame.image.load('fire.png'),(128,128))
fw1 = pygame.transform.scale(pygame.image.load('fire1.png'),(128,128))
nxt = pygame.transform.scale(pygame.image.load('next.png'),(80,80))

pygame.display.set_caption('Two Cars')


rcarpos = 2
ycarpos = 1
yind = 0
yneg = 1
rind = 0
rneg = 1


def drawLine():
    for i in range(1, 4):
        if i == 2:
            width = 4
        else:
            width = 2
        pygame.draw.line(screen, (255, 255, 255),
                         (i*125, 0), (i*125, height), width)


def posRcar():
    global rx
    if rlturn:
        if rcarpos == 2:
            rx = 250+(rloop*25) + math.floor((125-carpx)/2)
            screen.blit(rcar[rind], (250+(rloop*25) +
                                     math.floor((125-carpx)/2), carpos + (rind * 9)))
        if rcarpos == 3:
            rx = 375-(rloop*25) + math.floor((125-carpx)/2)
            screen.blit(rcar1[rind], (375-(rloop*25) +
                                      math.floor((125-carpx)/2), carpos + (rind * 9)))
    if not rlturn:
        rx = (rcarpos*125) + math.floor((125-carpx)/2)
        screen.blit(rcar[rind], ((rcarpos*125) +
                                 math.floor((125-carpx)/2), carpos))


def posYcar():
    global yx
    if ylturn:
        if ycarpos == 1:
            yx = 125-(yloop*25) + math.floor((125-carpx)/2)
            screen.blit(ycar[yind], (125-(yloop*25) +
                                     math.floor((125-carpx)/2), carpos + (yind * 9)))
        if ycarpos == 0:
            yx = 0+(yloop*25) + math.floor((125-carpx)/2)
            screen.blit(ycar1[yind], (0+(yloop*25) +
                                      math.floor((125-carpx)/2), carpos + (yind * 9)))
    if not ylturn:
        yx = (ycarpos*125) + math.floor((125-carpx)/2)
        screen.blit(ycar[yind], ((ycarpos*125) +
                                 math.floor((125-carpx)/2), carpos))


def random_placement():
    global way
    global ch
    global counter
    if counter == -gap and not (gameover or paused):
        ind = ScoreArr.index(None)
        # print(ind)
        ch = random.randint(0, 1)
        if way == 0:
            if ch == 0:
                ScoreArr[ind] = Point(random.randint(
                    0, 1), random.randint(-gap-scorepx, -scorepx))
            elif ch == 1:
                ScoreArr[ind] = Virus(random.randint(
                    0, 1), random.randint(-gap-scorepx, -scorepx))
            way = 1
        elif way == 1:
            if ch == 0:
                ScoreArr[ind] = Point(random.randint(
                    2, 3), random.randint(-gap-scorepx, -scorepx))
            elif ch == 1:
                ScoreArr[ind] = Virus(random.randint(
                    2, 3), random.randint(-gap-scorepx, -scorepx))
            way = 0
    for i in range(8):
        if ScoreArr[i]:
            if ScoreArr[i].move():
                ScoreArr[i] = None
    if not gameover and not paused:
        counter += speed
    # print(counter)
    if counter >= 0:
        counter = -gap

# def setInterval():
#     i=3
#     e = threading.Event()
#     while not e.wait(1):
#         print(i)
#         i-=1
#         if i==0:
#             break

rloop = 1
yloop = 1
ych = False
rch = False
pnt=pygame.transform.scale(pygame.image.load('point.png'), (100, 100))
vrs=pygame.transform.scale(pygame.image.load('virus.png'), (100, 100))
timi=3
while RUNNING:
    clock.tick(30)
    if begin:
        screen.fill((0, 140, 255))
        txt = raleway_30.render(name.upper(),True,(255,255,255))
        a = screen.blit(txt,(30,480))
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                conn.close()
                pygame.quit()
                sys.exit(0)
            if eve.type == pygame.KEYDOWN:
                    # print(eve.key)
                    if (eve.key >= 97 or eve.key <= 122) and eve.key != 8 and eve.key != 13 and a.width<=420:
                        # print(a.width)
                        name += chr(eve.key)
                    if eve.key == 8 and len(name)>0:
                        name = name[:len(name)-1]
                    if eve.key == 13 and len(name)>0:
                        c.execute("""
                            INSERT INTO detail VALUES( :name , :score , :k , :d )
                        """,{"name":name,"score":0,"k":107,"d":100})
                        conn.commit()
                        # conn.close()
                        begin=False
                        info=True

        if go % 40 == 0:
            pygame.draw.line(screen, (255, 255, 255),(a.width,520),(30+a.width,520),0)
        else :
            pygame.draw.line(screen, (255, 255, 255),(30+a.width,520),(30+a.width+20,520),5)
        screen.blit(fw1,(20+go,180))
        screen.blit(fw,(360-go,180))
        if go == 360:
            go = 0
        go += 10
    elif info:
        screen.fill((255,215,0))
        nx=screen.blit(nxt,(400,30))
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                conn.close()
                pygame.quit()
                sys.exit(0)
        screen.blit(pnt,(30,80))
        txt1 = raleway_20.render('Catch me',True,(0,0,0))
        txt2 = raleway_20.render('Dodge me',True,(0,0,0))
        screen.blit(vrs,(30,230))
        screen.blit(txt1,(150,110))
        screen.blit(txt2,(150,260))
        txt3 = raleway_30.render('Default Controls:',True,(0,0,0))
        screen.blit(txt3,(10,380))
        txt4 = raleway_20.render('Yellow  D',True,(0,0,0))
        screen.blit(txt4,(20,430))
        txt5 = raleway_20.render('Red        K',True,(0,0,0))
        screen.blit(txt5,(20,470))
        txt7 = raleway_20.render('Pause   SPACE',True,(0,0,0))
        screen.blit(txt7,(20,510))
        txt6 = raleway_15.render("Can change them in the settings",True,(130,130,130))
        screen.blit(txt6,(20,620))

        if pygame.mouse.get_pressed()[0]:
            mpos=pygame.mouse.get_pos()
            if nx.collidepoint(mpos[0],mpos[1]) :
                info = False
        
        
    else:
        text = raleway_30.render(str(score), True,(255, 255, 255))
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                conn.close()
                pygame.quit()
                sys.exit(0)
            if eve.type == pygame.KEYDOWN and stng :
                # print(eve.key)
                if eve.key >= 97 or eve.key <= 122:
                    if rch and eve.key != YKEY:
                        RKEY = eve.key
                        c.execute("UPDATE detail SET RKEY=:r",{"r":RKEY})
                        conn.commit()
                        rch = False
                    elif ych and eve.key != RKEY:
                        YKEY = eve.key
                        c.execute("UPDATE detail SET RKEY=:r",{"r":RKEY})
                        conn.commit()
                        ych = False
                
            if eve.type == pygame.KEYUP and not gameover and not start and not stng and not paused:
                if eve.key == YKEY:
                    ylturn = True
                    yneg = 1
                if eve.key == RKEY:
                    rlturn = True
                    rneg = 1
                if eve.key == 32:
                    paused = True
        if ylturn:
            if yind == 2:
                yneg = -1
            yind += yneg
            yloop += 1
            if yind == 0:
                ylturn = False
                yloop = 1
                ycarpos = 0 if ycarpos == 1 else 1

        if rlturn:
            if rind == 2:
                rneg = -1
            rind += rneg
            rloop += 1
            if rind == 0:
                rlturn = False
                rloop = 1
                rcarpos = 3 if rcarpos == 2 else 2

        screen.fill((0, 140, 255))
        drawLine()
        screen.blit(text,(420,30))
        posRcar()
        posYcar()
        if not start :
            random_placement()
        
        if gameover and not stng:
            tx=''
            if score > best:
                best = score
                c.execute("""UPDATE detail SET score=:sc""",{"sc":score})
                conn.commit()
            tx = "Hey "
            txt = raleway_15.render("BEST "+str(best),True,(255,255,255))
            txt1 = raleway_15.render("SCORE "+str(score),True,(255,255,255))
            txt2 = raleway_20.render(tx+name.upper(),True,(255,255,255))
            goscreen = pygame.Surface((500,800))
            goscreen.fill((0,0,0))
            for i in range(50,200,1):
                goscreen.set_alpha(i)
            screen.blit(goscreen,(0,0))
            got = raleway.render('GAME OVER',True,(255,255,255)) 
            screen.blit(got,(40,170))
            scr = screen.blit(settings,(124,380))
            res = screen.blit(restart,(312,380))
            screen.blit(txt1,(195,600))
            screen.blit(txt,(195,650))
            screen.blit(txt2,(math.floor((500-txt2.get_rect().width)/2),520))
            if pygame.mouse.get_pressed()[0]:
                mpos=pygame.mouse.get_pos()
                if res.collidepoint(mpos[0],mpos[1]):
                    gameover=False
                    score = 0
                    ScoreArr=[None]*16
                    speed = 17
                    ycarpos=1
                    rcarpos=2
                elif scr.collidepoint(mpos[0],mpos[1]):
                    stng = True
        if timer:
            
            timscreen = pygame.Surface((500,800))
            timscreen.fill((0,0,0))
            timscreen.set_alpha(200)
            screen.blit(timscreen,(0,0))
            # pygame.display.update()
            # print(i)
            txt_surf = raleway.render(str(timi), True, (255,255,255))
            alpha_img = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
            for j in range(1,255):
                alpha_img.fill((255, 255, 255, 255-j))
                txt_surf.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(txt_surf,(220,370))
            pygame.display.update()            
            timi-=1
            time.sleep(1)
            if timi==0:
                timi=3
                timer = False
                paused = False
            
        if (start or paused) and not stng and not timer:
            stscreen = pygame.Surface((500,800))
            stscreen.fill((0,0,0))
            for i in range(50,200,1):
                stscreen.set_alpha(i)
            screen.blit(stscreen,(0,0))
            got = raleway.render('PLAY',True,(255,255,255)) if start else raleway.render('PAUSED',True,(255,255,255))
            if paused :
                screen.blit(got,(100,170))
            else:    
                screen.blit(got,(140,170))
            ply = screen.blit(play,(124,380))
            scr = screen.blit(settings,(312,380))
            if pygame.mouse.get_pressed()[0]:
                mpos=pygame.mouse.get_pos()
                if ply.collidepoint(mpos[0],mpos[1]):
                    start = False
                    if paused:
                        timer = True
                    
                elif scr.collidepoint(mpos[0],mpos[1]):
                    stng = True
        
        if stng:
            stnscreen = pygame.Surface((500,800))
            stnscreen.fill((0,0,0))
            for i in range(50,200,1):
                stnscreen.set_alpha(i)
            screen.blit(stnscreen,(0,0))        
            got = raleway.render('SETTINGS',True,(255,255,255)) 
            screen.blit(got,(80,170))
            bck = screen.blit(back,(30,680))
            screen.blit(jstick,(200,30))
            cir1=screen.blit(c1,(33,380))
            cir2=screen.blit(c2,(266,380))
            yk = raleway.render(chr(YKEY-32),True,(255,255,255))
            rk = raleway.render(chr(RKEY-32),True,(255,255,255))
            screen.blit(rk,(112,440))
            screen.blit(yk,(345,440))
            if pygame.mouse.get_pressed()[0]:
                mpos=pygame.mouse.get_pos()
                if bck.collidepoint(mpos[0],mpos[1]):
                    stng = False
                if cir1.collidepoint(mpos[0],mpos[1]):
                    # print('c1')
                    rch = True
                    ych = False
                if cir2.collidepoint(mpos[0],mpos[1]):
                    # print('c2')
                    ych = True
                    rch = False

        if score % 10 == 9:
            inc=1
        if score % 10 ==0 and score != 0 and inc:
            speed += inc
            inc = 0
    pygame.display.update()
