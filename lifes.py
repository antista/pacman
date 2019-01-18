#!/usr/bin/env python
# from pacman import *
import pygame
from pygame import *
from const import SIZE, BACK_COLOR


class Life(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, SIZE, SIZE)
        self.image = Surface((SIZE, SIZE))
        self.image.fill(Color(BACK_COLOR))
        self.image.set_colorkey(Color(BACK_COLOR))
        self.image = image.load('images/pacman32.png')

    def draw(self, screen):
        '''Рисует значок жизни'''
        screen.blit(self.image, (self.rect.x, self.rect.y))

    @staticmethod
    def print(field):
        '''Отображает значки жизни на экране'''
        x = field.win_width - 150
        pygame.init()
        font = pygame.font.Font(None, 40)
        text = font.render("x" + str(field.hero.lifes_count), True, pygame.Color("#999999"))
        field.screen.blit(text, [x + 60, field.win_height - 80])
        for i in range(field.hero.lifes_count):
            l = Life(x + 30, field.win_height - 50)
            l.draw(field.screen)
            x += 30
