import pyxel

from shared_constants import (
    GUNSHOT_START_RADIUS,
    GUNSHOT_END_RADIUS,
    GUNSHOT_COLOR_IN,
    GUNSHOT_COLOR_OUT,
)


class Gunshot:
    def __init__(self, gunshots, x, y):
        self.x = x
        self.y = y
        self.radius = GUNSHOT_START_RADIUS
        self.active = True
        gunshots.append(self)

    def update(self):
        self.radius += 1
        if self.radius > GUNSHOT_END_RADIUS:
            self.active = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, GUNSHOT_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, GUNSHOT_COLOR_OUT)
