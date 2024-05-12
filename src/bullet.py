import pyxel

from shared_constants import BULLET_HEIGHT, BULLET_WIDTH, BULLET_SPEED, BULLET_COLOR


class Bullet:
    def __init__(self, bullets, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.active = True
        bullets.append(self)

    def update(self):
        self.y -= BULLET_SPEED
        if self.y + self.h - 1 < 0:
            self.active = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)
