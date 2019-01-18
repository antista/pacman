import pygame
from pygame import *
from const import SIZE, BACK_COLOR


class Entity(sprite.Sprite):
    def __init__(self, x, y, speed=2):
        '''Инициализирует сущность'''
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.image = Surface((SIZE, SIZE))
        self.image.fill(Color(BACK_COLOR))
        self.rect = Rect(x, y, SIZE, SIZE)
        self.image.set_colorkey(Color(BACK_COLOR))
        self.current_dir = 'left'
        self.speed = speed

    def update_move(self):
        '''Изменяет текущие координаты сущности'''
        if self.current_dir == 'left':
            self.rect.x -= self.speed
        elif self.current_dir == 'right':
            self.rect.x += self.speed
        elif self.current_dir == 'up':
            self.rect.y -= self.speed
        elif self.current_dir == 'down':
            self.rect.y += self.speed

    def move_in_exits(self, exits):
        '''Отвечает за перемещение сущности через туннели по бокам поля'''
        if exits != []:
            if self.rect.x <= exits[0] - 2:
                self.rect.x = exits[1] + 4
            if self.rect.x >= exits[1] + 8:
                self.rect.x = exits[0] + 2
