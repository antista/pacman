# import pygame
from pygame import *
from const import SIZE
# from pacman import *

PLATFORM_SIZE = SIZE
PLATFORM_COLOR = '#061374'  # '#0A1694'#"#FF6262"
GATE_SIZE = SIZE / 4
GATE_COLOR = '#EAAEE5'  # "#F1D5F0"


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_SIZE, PLATFORM_SIZE))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_SIZE, PLATFORM_SIZE)


class Gate(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_SIZE, GATE_SIZE))
        self.image.fill(Color(GATE_COLOR))
        self.rect = Rect(x, y, PLATFORM_SIZE, GATE_SIZE)
