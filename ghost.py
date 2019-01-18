#!/usr/bin/env python
from pacman import *
from math import sqrt
from entity import *
import random


class Ghost(Entity):
    def __init__(self, name, x, y, win_width = 0, win_height=0):
        '''Инициализирует приведение-монстра'''
        super().__init__(x, y)
        self.name = name
        self.image = self.default_image = image.load('images/ghosts/' + name + '.ico')
        self.scared_image = image.load('images/ghosts/scared.ico')
        self.dead_image = image.load('images/ghosts/dead.ico')
        self.alive = True
        self.is_in_house = True
        self.scared = self.was_ate = False
        if name == 'blinky':
            self.default_target = (win_width - 9 * SIZE, -SIZE)
        if name == 'pinky':
            self.default_target = (11 * SIZE, -SIZE)
        if name == 'inky':
            self.default_target = (win_width - 9 * SIZE, win_height + SIZE)
        if name == 'klyde':
            self.default_target = (11 * SIZE, win_height + SIZE)
        self.target = self.default_target

    def decide_direction(self, platforms):
        '''Производит принятие решения о следующем направлении'''
        d = self.current_dir
        min = 99999999999
        for i in ['left', 'right', 'up', 'down']:
            turn = True
            tmp = Ghost(self.name, self.rect.x, self.rect.y)
            tmp.current_dir = i
            tmp.update_move()
            for p in platforms:
                if sprite.collide_rect(tmp, p):
                    turn = False
            if not turn:
                continue
            t = sqrt((tmp.rect.x - self.target[0]) * (tmp.rect.x - self.target[0]) +
                     (tmp.rect.y - self.target[1]) * (tmp.rect.y - self.target[1]))
            if t < min and (
                    (self.current_dir == 'left' and i != 'right') or
                    (self.current_dir == 'right' and i != 'left') or
                    (self.current_dir == 'up' and i != 'down') or
                    (self.current_dir == 'down' and i != 'up')):
                d = i
                min = t
        self.current_dir = d

    def update(self, field):
        '''Обновляет состояние привидения-монстра'''
        if self.scared:
            self.scare(field)
            self.image = self.scared_image
        elif self.alive and self.rect.x % SIZE == 0 and self.rect.y % SIZE == 0:
            self.image = self.default_image
            self.change_target(field, field.timer.interval)
            self.speed = 2
        if not self.alive:
            self.dead(field)
        if self.rect.x % SIZE == 0 and self.rect.y % SIZE == 0:
            self.decide_direction(field.platforms)
        self.update_move()
        self.move_in_exits(field.exits)

    def change_target(self, field, time):
        '''Изменяет цель привидения-монстра'''
        if time == 7:
            self.target = self.default_target
        else:
            self.find_target(field)

    def dead(self, field):
        '''Смерть привидения-монстра'''
        self.scared = False
        self.image = self.dead_image
        self.was_ate = True if not field.hero.endless_energy else False
        if self.rect.x % SIZE == 0 and self.rect.y % SIZE == 0:
            self.speed = 4
        self.free(field.gates) if not field.hero.endless_energy else self.free(field.gates,True)

    def free(self, gates, scared=False):
        '''Освобождет привидение-монстра из домика'''
        if self.rect.x != gates[0] or self.rect.y != gates[1]:
            self.target = (gates[0], gates[1] - SIZE - SIZE)
        elif self.rect.x == gates[0] and self.rect.y == gates[1]:
            self.target = self.default_target
            self.is_in_house = False
            self.alive = True
            self.speed = 2
            self.scared = scared
            self.image = self.default_image if not scared else self.scared_image

    def find_target(self, field):
        '''Ищет цель для каждого приведения-монстра в зависимости от его алгоритма'''
        if self.name == 'blinky':
            self.target = (field.hero.rect.x, field.hero.rect.y)
        if self.name == 'pinky' and not self.is_in_house:
            self.target = (field.hero.rect.x + field.hero.xvel * 2, field.hero.rect.y + field.hero.yvel * 2)
        if self.name == 'inky' and not self.is_in_house:
            self.target = (
                field.blinky.rect.x + (field.hero.rect.x + field.hero.xvel / 2 * SIZE - field.blinky.rect.x) * 2,
                field.blinky.rect.y + (field.hero.rect.y + field.hero.yvel / 2 * SIZE - field.blinky.rect.y) * 2)
        if self.name == 'klyde' and not self.is_in_house:
            if sqrt((self.rect.x - field.hero.rect.x) * (self.rect.x - field.hero.rect.x) +
                    (self.rect.y - field.hero.rect.y) * (self.rect.y - field.hero.rect.y)) > 8 * SIZE:
                self.target = (field.hero.rect.x, field.hero.rect.y)
            else:
                self.target = self.default_target

    def scare(self, field):
        '''Метод поиска цели в режиме испуга'''
        self.target = (random.randint(0, field.win_width), random.randint(0, field.win_height))
