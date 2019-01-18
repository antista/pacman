#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyganim
from pygame import *
from pyganim import *
from const import *
from entity import *
from timer import Timer
# import pyaudio


class Pacman(Entity):
    def __init__(self, x, y):
        '''Инициалзирует пакмана'''
        super().__init__(x, y, speed=4)
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.startX = x
        self.startY = y
        self.next_dir = None
        self.eated_dots_count = self.energizer_eated = 0
        self.energizer = False
        self.lifes_count = 3
        self.timer = None
        self.invincible = False
        self.endless_energy = False
        pygame.mixer.init()
        self.sound_effects = {
            name: pygame.mixer.Sound(sound)
            for name, sound in SOUNDS.items()}
        self.init_anim()

    def init_anim(self):
        '''Инициализирует анимацию движения пакмана'''
        self.boltAnim = dict()
        for direction in ANIMATION:
            boltAnim = []
            for picture in ANIMATION[direction]:
                boltAnim.append((picture, ANIMATION_DELAY))
            self.boltAnim[direction] = pyganim.PygAnimation(boltAnim)
            self.boltAnim[direction].play()

        self.boltAnim['stay'] = None


    def update(self, field):
        '''Обновляет состояние пакмана'''
        self.update_move()
        self.update_animation()
        self.move_in_exits(field.exits)
        self.collide(field)
        self.check_dead(field)
        if self.timer is not None and self.timer.check_time() and not self.endless_energy:
            self.energizer = False
            self.timer = None


    def update_animation(self):
        '''Обновляет анимацию движения пакмана'''
        self.image.fill(Color(BACK_COLOR))
        if self.current_dir is not None:
            self.boltAnim[self.current_dir].blit(self.image, (0, 0))
        else:
            self.boltAnim['stay'].blit(self.image, (0, 0))

    def collide(self, field):
        '''Проверяет наличие столкновения пакмана с объектами поля и обрабатывает их'''
        tmp = self
        if self.next_dir is not None:
            tmp = Pacman(self.rect.x, self.rect.y)
            tmp.current_dir = self.next_dir
            tmp.update_move()
        turn = True
        for p in field.platforms:
            if sprite.collide_rect(self, p):
                if self.current_dir == 'left':
                    self.rect.left = p.rect.right
                if self.current_dir == 'right':
                    self.rect.right = p.rect.left
                if self.current_dir == 'up':
                    self.rect.top = p.rect.bottom
                if self.current_dir == 'down':
                    self.rect.bottom = p.rect.top
                self.boltAnim['stay'] = pyganim.PygAnimation(ANIMATION_STAY[self.current_dir])
                self.boltAnim['stay'].play()
                self.boltAnim['stay'].blit(self.image, (0, 0))
                if self.next_dir is not None:
                    self.current_dir = self.next_dir
                    self.next_dir = None
                else:
                    self.current_dir = None
            if sprite.collide_rect(tmp, p):
                turn = False

        if self.next_dir is not None and turn:
            self.current_dir = self.next_dir
            self.next_dir = None

        if len(pygame.sprite.spritecollide(self, field.dots, False)) != 0:
            self.sound_effects['wakka'].play(maxtime=200)
            pygame.time.wait(50)
            self.eated_dots_count += len(pygame.sprite.spritecollide(self, field.dots, True))

        if len(pygame.sprite.spritecollide(self, field.energizers, True)) != 0:
            pygame.mixer.Sound(SOUNDS['energizer']).play()
            self.energizer = True
            self.timer = Timer(15)
            self.energizer_eated += 1
            for ghost in field.ghosts:
                if ghost is not None:
                    ghost.was_ate = False

    def dead(self, field):
        '''События при смерти пакмана'''
        pygame.mixer.Sound(SOUNDS['death']).play()
        self.rect.x = self.startX
        self.rect.y = self.startY
        self.lifes_count -= 1
        self.current_dir = 'left'
        self.timer = None
        self.energizer = False
        field.init_ghosts()
        pygame.time.wait(2000)

    def check_dead(self, field):
        '''Проверка на смерть пакмана'''
        for ghost in field.ghosts:
            if ghost is not None and sprite.collide_rect(self, ghost):
                if not self.energizer and not self.invincible:
                    self.dead(field)
                elif self.energizer:
                    if sprite.collide_rect(self, ghost) and ghost.alive:
                        if not ghost.was_ate:
                            self.sound_effects['eat_ghost'].play()
                            ghost.alive = False
                            self.energizer_eated += 4
                        elif not self.invincible:
                            self.dead(field)
