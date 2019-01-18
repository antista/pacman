import pyganim
from pygame import *
from pyganim import *

SOUNDS = dict(
    wakka='sounds/wakka.wav',
    energizer='sounds/energizer.wav',
    eat_ghost='sounds/eating_ghost.wav',
    death='sounds/death.wav'
)

SIZE = 16
BACK_COLOR = "#00FFFF"
ANIMATION_DELAY = 50  # скорость смены кадров

ANIMATION = dict()

ANIMATION['right'] = [('images/moving/m1.ico'),
                      ('images/moving/m2.ico'),
                      ('images/moving/m3.ico'),
                      ('images/moving/m4.ico'),
                      ('images/moving/m5.ico'),
                      ('images/moving/m6.ico'),
                      ('images/moving/m6.ico'),
                      ('images/moving/m5.ico'),
                      ('images/moving/m4.ico'),
                      ('images/moving/m3.ico'),
                      ('images/moving/m2.ico'),
                      ('images/moving/m1.ico')]

ANIMATION['left'] = [pygame.transform.rotate(image.load('images/moving/m1.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m2.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m3.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m4.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m5.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m6.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m6.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m5.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m4.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m3.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m2.ico'), 180),
                     pygame.transform.rotate(image.load('images/moving/m1.ico'), 180)]

ANIMATION['up'] = [pygame.transform.rotate(image.load('images/moving/m1.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m2.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m3.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m4.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m5.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m6.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m6.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m5.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m4.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m3.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m2.ico'), 90),
                   pygame.transform.rotate(image.load('images/moving/m1.ico'), 90)]

ANIMATION['down'] = [pygame.transform.rotate(image.load('images/moving/m1.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m2.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m3.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m4.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m5.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m6.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m6.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m5.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m4.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m3.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m2.ico'), -90),
                     pygame.transform.rotate(image.load('images/moving/m1.ico'), -90)]

ANIMATION_STAY = dict()

ANIMATION_STAY['left'] = [(pygame.transform.rotate(image.load('images/moving/m6.ico'), 180), 1)]
ANIMATION_STAY['right'] = [('images/moving/m6.ico', 1)]
ANIMATION_STAY['up'] = [(pygame.transform.rotate(image.load('images/moving/m6.ico'), 90), 1)]
ANIMATION_STAY['down'] = [(pygame.transform.rotate(image.load('images/moving/m6.ico'), -90), 1)]
