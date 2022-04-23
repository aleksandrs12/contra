import pygame
from export import Player
from export import Platform
import keyboard
import time


pygame.init()
can_press = {
    's': True,
    'down': True,
    'shift': True,
    'rshift': True,
    'rctrl': True,
    'ctrl': True
}
font = pygame.font.Font('pixel.ttf', 60)
run = True
win = pygame.display.set_mode((1200, 900))

a = Player([50, 100], 100, 10, 29, 0, 1)
b = Player([1150, 100], 100, 10, 29, 0, -1)
plats = [Platform(0, 300, 100, 30), Platform(1100, 300, 100, 30), Platform(590, 200, 20, 100), Platform(70, 600, 150, 20), Platform(980, 600, 150, 20), 
         Platform(320, 550, 150, 20), Platform(730, 550, 150, 20), Platform(550, 300, 100, 20), Platform(0, 800, 1200, 100),
         Platform(525, 450, 150, 20), Platform(-20, -300, 24, 1200), Platform(1196, -300, 40, 1200)]
bullets = []

while run:
    if a.pos[0] < 4:
        a.pos[0] = 4

    if b.pos[0] < 4:
        b.pos[0] = 4

    if a.pos[0] > 1160:
        a.pos[0] = 1157

    if b.pos[0] > 1160:
        b.pos[0] = 1157
    pygame.draw.rect(win, (8, 8, 24), (0, 0, 1200, 900))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if keyboard.is_pressed('w'):
        a.jump(plats)
    if keyboard.is_pressed('a'):
        a.pos[0] -= a.speed
        a.is_moving = True
        a.dir = -1
    if keyboard.is_pressed('d'):
        a.pos[0] += a.speed
        a.is_moving = True
        a.dir = 1
    if keyboard.is_pressed('s'):
        if can_press['s']:
            a.shoot(bullets)
            can_press['s'] = False
    else:
        can_press['s'] = True
    if keyboard.is_pressed('left shift'):
        if can_press['shift']:
            a.art(bullets)
            can_press['shift'] = False
    else:
        can_press['shift'] = True
    

    if keyboard.is_pressed('up'):
        b.jump(plats)
    if keyboard.is_pressed('left'):
        b.pos[0] -= b.speed
        b.is_moving = True
        b.dir = -1
    if keyboard.is_pressed('right'):
        b.pos[0] += b.speed
        b.is_moving = True
        b.dir = 1
    if keyboard.is_pressed('down'):
        if can_press['down']:
            b.shoot(bullets)
            can_press['down'] = False
    else:
        can_press['down'] = True
    if keyboard.is_pressed('right shift'):
        if can_press['rshift']:
            b.art(bullets)
            can_press['rshift'] = False
    else:
        can_press['rshift'] = True

    '''
    if keyboard.is_pressed('right ctrl'):
        if can_press['rctrl']:
            b.shield(win)

    if keyboard.is_pressed('left ctrl'):
        if can_press['ctrl']:
            a.shield(win)
    '''
    

    for n in plats:
        n.render(win)

    a.physics(plats)
    b.physics(plats)
    a.render(win, plats)
    b.render(win, plats)


    for n in bullets:
        n.render(win)
        if n.move(a, b, bullets):
            bullets.pop(bullets.index(n))
        
    for n in range(1, len(bullets)+1):
        try:
            if bullets[-n].on_plat(plats):
                bullets.pop(-n)

            elif bullets[-n].hit(a):
                a.hp -= 10
                bullets.pop(-n)
            elif bullets[-n].hit(b):
                b.hp -= 10
                bullets.pop(-n)
        except:
            pass

    if a.hp < 1 and not b.hp < 1:
        text = font.render('player  2  won', True, (150, 150, 150))
        textRect = text.get_rect()
        textRect.center = (600, 400)
        win.blit(text, textRect)

    elif b.hp < 1:
        text = font.render('player  1  won', True, (150, 150, 150))
        textRect = text.get_rect()
        textRect.center = (600, 400)
        win.blit(text, textRect)


    b.can_hit = True
    a.can_hit = True
    pygame.display.update()
    time.sleep(0.02)
pygame.quit

