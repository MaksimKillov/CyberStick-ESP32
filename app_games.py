from core import *
import random

def snake_game():
    W,H = 16,8; CW,CH = 8,8
    snake = [(8,4),(7,4),(6,4)]
    direction = (1,0)
    food = (random.randint(0,W-1), random.randint(0,H-1))
    score = 0; speed = 200
    def draw():
        cls()
        for x,y in snake: fill_rect(x*CW,y*CH,CW-1,CH-1)
        fx,fy = food; fill_rect(fx*CW+2,fy*CH+2,4,4)
        txt("S:"+str(score),90,0); show()
    def gameover():
        cls(); border(); txt("GAME OVER",25,18); txt("Score:"+str(score),30,32); txt("OK=Menu",35,48); show(); wait_ok()
    while True:
        if btn_left.value()==0: direction=(direction[1],-direction[0]); time.sleep_ms(120)
        if btn_right.value()==0: direction=(-direction[1],direction[0]); time.sleep_ms(120)
        if btn_pressed(btn_ok): return
        hx,hy=snake[0]; nx,ny=hx+direction[0],hy+direction[1]
        if nx<0 or nx>=W or ny<0 or ny>=H or (nx,ny) in snake: gameover(); return
        snake.insert(0,(nx,ny))
        if (nx,ny)==food:
            score+=1; speed=max(80,speed-5)
            while True:
                fx=random.randint(0,W-1); fy=random.randint(0,H-1)
                if (fx,fy) not in snake: food=(fx,fy); break
        else: snake.pop()
        draw(); time.sleep_ms(speed)

def flappy_bird():
    by = 32; bvy = 0; pipes = []; frame = 0; score = 0; alive = True
    GAP = 20; PIPE_W = 8; SPEED = 2
    def add_pipe(): pipes.append([128, random.randint(10, 44)])
    add_pipe()
    def draw():
        cls(); fill_rect(20, int(by)-3, 7, 6)
        for p in pipes: oled.fill_rect(p[0], 0, PIPE_W, p[1]-GAP//2, 1); oled.fill_rect(p[0], p[1]+GAP//2, PIPE_W, 64-(p[1]+GAP//2), 1)
        txt("S:"+str(score), 90, 0); show()
    def gameover(): cls(); border(); txt("GAME OVER", 25, 18); txt("Score:"+str(score), 30, 32); txt("OK=Menu", 35, 48); show(); wait_ok()
    last = time.ticks_ms()
    while alive:
        now = time.ticks_ms()
        if time.ticks_diff(now, last) < 50: time.sleep_ms(5); continue
        last = now
        if btn_ok.value()==0: bvy = -4
        if btn_pressed(btn_left): return
        bvy += 0.5; by += bvy
        if by < 0 or by > 64: gameover(); return
        for p in pipes: p[0] -= SPEED
        if pipes and pipes[0][0] < -PIPE_W: pipes.pop(0); score += 1; add_pipe()
        frame += 1
        if frame % 60 == 0: add_pipe()
        bx = 20
        for p in pipes:
            if bx+7 > p[0] and bx < p[0]+PIPE_W:
                if by-3 < p[1]-GAP//2 or by+3 > p[1]+GAP//2: gameover(); return
        draw()

def dino_game():
    dy = 52; dvy = 0; on_ground = True; cacti = []; frame = 0; score = 0; SPEED = 2
    def add_cactus(): cacti.append([128, random.randint(8,18)])
    add_cactus()
    def draw():
        cls(); hline(0, 58, 128); fill_rect(15, int(dy)-10, 10, 10); fill_rect(17, int(dy), 6, 4)
        for c in cacti: fill_rect(c[0], 58-c[1], 7, c[1])
        txt("S:"+str(score), 90, 0); show()
    def gameover(): cls(); border(); txt("GAME OVER", 25, 18); txt("Score:"+str(score), 30, 32); txt("OK=Menu", 35, 48); show(); wait_ok()
    last = time.ticks_ms()
    while True:
        now = time.ticks_ms()
        if time.ticks_diff(now, last) < 40: time.sleep_ms(5); continue
        last = now
        if (btn_ok.value()==0 or btn_right.value()==0) and on_ground: dvy = -5; on_ground = False
        if btn_pressed(btn_left): return
        dvy += 0.6; dy += dvy
        if dy >= 52: dy = 52; dvy = 0; on_ground = True
        for c in cacti: c[0] -= SPEED
        if cacti and cacti[0][0] < -8: cacti.pop(0); score += 1
        frame += 1
        if frame % 80 == 0: add_cactus()
        for c in cacti:
            if c[0] < 25 and c[0]+7 > 15:
                if dy > 58-c[1]-5: gameover(); return
        draw()