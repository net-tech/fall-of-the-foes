import pyxel

from shared_constants import ENEMY_SPEED, ENEMY_HEIGHT, ENEMY_WIDTH


class Enemy:
    def __init__(self, enemies, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.timer_offset = pyxel.rndi(0, 59)
        self.active = True
        enemies.append(self)

    def update(self, enemies):
        if (pyxel.frame_count + self.timer_offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1
        self.y += ENEMY_SPEED
        if self.y > pyxel.height - 1:
            self.active = False
            position = enemies.index(self)
            del enemies[position]

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)
