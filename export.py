import pygame


animations = {
    1: pygame.image.load('animation_1.png'),
    2: pygame.image.load('animation_2.png'),
    3: pygame.image.load('animation_3.png')
}

class Player:
    is_moving = True
    animation = 1
    can_hit = True
    def __init__(self, pos, hp, speed, jumph, grav, dir):
        self.pos = pos
        self.hp = hp
        self.speed = speed
        self.jumph = jumph
        self.grav = grav
        self.dir  = dir

    def jump(self, plats):
        if self.on_plat(plats):
            self.grav = -self.jumph

    def render(self, win, plats):
        pygame.Surface.blit(win, animations[self.animation], self.pos)

        if self.is_moving and self.on_plat(plats):
            if self.animation != 3:
                self.animation += 1
            else:
                self.animation = 1
        self.is_moving = False

    def shield(self, win):
        pygame.draw.rect(win, (210, 200, 200), (self.pos[0]-10, self.pos[1]-10, 59, 104))
        pygame.draw.rect(win, (8, 8, 24), (self.pos[0], self.pos[1], 39, 84))
        self.can_hit = False


    def physics(self, plats):
        if self.grav > 17:
            if self.onplat2(plats):
                self.grav = 0
            else:
                self.grav += 2
            self.pos[1] += self.grav
        else:
            if self.on_plat(plats):
                self.grav = 0
            else:
                self.grav += 2
            self.pos[1] += self.grav
        if self.on_plat(plats):
            self.wall(plats)


    def on_plat(self, plats):
        for n in plats:
            if self.grav >= 0 and n.y <= self.pos[1] + animations[self.animation].get_height() and n.y + 20 >= self.pos[1] + animations[self.animation].get_height() and n.x <= self.pos[0] + animations[self.animation].get_width() and n.x + n.lenx > self.pos[0]:
                self.pos[1] = n.y - animations[self.animation].get_height()
                return True


    def shoot(self, l):
        l.append(Bullet(self.dir, self.pos[1]+20, self.pos[0] + 20 + 40 * self.dir, len(l)+1, 0, 15, 0, False))

    def onplat2(self, plat):
        for n in plat:
            if n.y > self.pos[1] and n.y < self.pos[1] + 85:
                if n.x <= self.pos[0] + animations[self.animation].get_width() and n.x + n.lenx > self.pos[0]:
                    self.pos[1] = n.y - animations[self.animation].get_height()
                    return True

    def wall(self, plat):
        for n in plat:
            if n.leny > n.lenx:
                if n.x < self.pos[0] + 39 and n.x + n.lenx > self.pos[0] and n.y + n.leny <= self.pos[1]+84+84 and n.y >= self.pos[1]-65:
                    self.pos[0] += self.dir * self.speed * -1

    def art(self, l):
        l.append(Bullet(self.dir, self.pos[1]+20, self.pos[0] + 20 + 40 * self.dir, len(l)+1, -29, 23, 2, True))


class Bullet:
    def __init__(self, dir, y, x, list_pos, grav, speed, diry, guided):
        self.dir = dir
        self.y = y
        self.x = x
        self.list_pos = list_pos
        self.grav = grav
        self.speed = speed
        self.diry = diry
        self.guided = guided

    def move(self, a, b, l):
        self.x += self.dir*self.speed
        self.y += self.grav
        if self.grav != 0:
            self.grav += 2
        self.y += self.diry
        if self.guided:
            if self.grav > 0:
                if ((a.pos[0] - self.x)**2 + (a.pos[1] - self.y)**2)**0.5 < 100:
                    l.append(Bullet(1, self.y, self.x, len(l)+1, -9, 5, 0, False))
                    l.append(Bullet(1, self.y, self.x, len(l)+1, -11, 0, 0, False))
                    l.append(Bullet(-1, self.y, self.x, len(l)+1, -11, 0, 0, False))
                    l.append(Bullet(-1, self.y, self.x, len(l)+1, -9, 5, 0, False))
                    return True
                if ((b.pos[0] - self.x)**2 + (b.pos[1] - self.y)**2)**0.5 < 100:
                    l.append(Bullet(1, self.y, self.x, len(l)+1, -9, 5, 0, False))
                    l.append(Bullet(1, self.y, self.x, len(l)+1, -11, 2, 0, False))
                    l.append(Bullet(-1, self.y, self.x, len(l)+1, -11, 2, 0, False))
                    l.append(Bullet(-1, self.y, self.x, len(l)+1, -9, 5, 0, False))
                    return True

        return False

    def on_plat(self, plat):
        for n in plat:
            if n.y <= self.y + 10 and n.y + n.leny >= self.y + 10 and n.x <= self.x + 10 and n.x + n.lenx > self.x:
                return True

    def render(self, win):
        pygame.draw.rect(win, (160, 20, 20), (self.x, self.y, 10, 10))

    def hit(self, p):
        if self.x + 10 >= p.pos[0] and self.x <= p.pos[0] + 40 and self.y + 10 >= p.pos[1] and self.y <= p.pos[1] + 85 and p.can_hit:
            
            return True


class Platform:
    def __init__(self, x, y, lenx, leny):
        self.x = x
        self.y = y
        self.lenx = lenx
        self.leny = leny

    def render(self, win):
        pygame.draw.rect(win, (154,205,50), (self.x, self.y, self.lenx, self.leny))

