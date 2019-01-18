# from pacman import *
from pygame import *

DOT_SIZE = 3
ENERGIZER_SIZE = 7
DOTS_COLOR = Color('#F8E3F8')


class Dot(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((DOT_SIZE, DOT_SIZE))
        self.image.fill(DOTS_COLOR)
        self.rect = Rect(x, y, DOT_SIZE, DOT_SIZE)


class Energizer(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((ENERGIZER_SIZE, ENERGIZER_SIZE))
        self.image.fill(DOTS_COLOR)
        self.rect = Rect(x, y, ENERGIZER_SIZE, ENERGIZER_SIZE)
