#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import *
from pacman import *
from platforms import *
from dots import *
from score import *
from lifes import *
from ghost import *
from candy import *
import menu
from timer import Timer
from icon import *


class Field():
    def __init__(self, map_source, last_score=0, lifes_left=3):
        '''Инициализирует поле со всеми сущностями в нем'''
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.name_map = map_source
        self.win_width = self.win_height = 0
        self.entities = pygame.sprite.Group()
        self.platforms, self.exits = [], []
        self.gates = None
        self.dots = pygame.sprite.Group()
        self.energizers = pygame.sprite.Group()
        self.hero = None
        self.init_map(map_source)
        if self.hero is not None:
            self.hero.lifes_count = lifes_left
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        self.bg = Surface((self.win_width, self.win_height))
        self.bg.fill(Color("#02030E"))
        self.blinky = self.pinky = self.inky = self.klyde = None
        self.ghosts = {self.blinky, self.pinky, self.inky, self.klyde}
        if self.gates is not None:
            self.init_ghosts()
        self.won = False
        self.score = Score(last_score)
        self.player_name = 'Player'
        self.active = True
        self.timer = Timer(7)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.klyde]
        self.candy = None
        self.music = pygame.mixer.Sound('sounds/music.wav')
        self.music_channel = None
        self.sound_icon = Icon()
        self.entities.add(self.sound_icon)

    def init_map(self, map_source):
        '''Инициализирует карту'''
        x = SIZE * 10
        y = 0
        map = open(map_source)
        for row in map:
            self.win_height += SIZE
            self.win_width = 20 * SIZE
            for col in row:
                self.win_width += SIZE
                if col == "w" or col == 'b':
                    pf = Platform(x, y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                if col == 'g':
                    g = Gate(x, y)
                    self.entities.add(g)
                    self.platforms.append(g)
                    if self.gates is None:
                        self.gates = (x, y - SIZE)
                    else:
                        self.gates = ((self.gates[0] + x) / 2, (self.gates[1] + y + SIZE) / 2 - SIZE)
                if col == '1':
                    self.exits.append(x)
                if col == '2':
                    self.exits.append(x)
                if col == '.':
                    d = Dot(x + (SIZE - DOT_SIZE) / 2, y + (SIZE - DOT_SIZE) / 2)
                    self.dots.add(d)
                    self.entities.add(d)
                if col == 'p':
                    self.hero = Pacman(x, y)
                    self.entities.add(self.hero)
                if col == 'e':
                    e = Energizer(x + (SIZE - ENERGIZER_SIZE) / 2, y + (SIZE - ENERGIZER_SIZE) / 2)
                    self.energizers.add(e)
                    self.entities.add(e)
                if col == 'c':
                    self.candy_coordinates = (x, y)

                x += PLATFORM_SIZE
            y += PLATFORM_SIZE
            x = SIZE * 10
        else:
            map.close()

    def process_events(self, events):
        '''Обрабатывает события нажатия клавиш, выигрыша и проигрыша'''
        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.time.wait(700)
                menu.Game.add_result(self)
                self.active = False
                menu.Game.ask_for_save(self)
                raise SystemExit('GOODBYE!!!')
            if e.type == KEYDOWN:
                if e.key == K_LEFT or e.key == K_a:
                    if self.hero.current_dir is None or self.hero.current_dir == 'right':
                        self.hero.current_dir = 'left'
                    elif self.hero.next_dir is None or self.hero.next_dir == 'right' or \
                            self.hero.current_dir == 'up' or self.hero.current_dir == 'down':
                        self.hero.next_dir = 'left'
                elif e.key == K_RIGHT or e.key == K_d:
                    if self.hero.current_dir is None or self.hero.current_dir == 'left':
                        self.hero.current_dir = 'right'
                    elif self.hero.next_dir is None or self.hero.next_dir == 'left' or \
                            self.hero.current_dir == 'up' or self.hero.current_dir == 'down':
                        self.hero.next_dir = 'right'
                if e.key == K_UP or e.key == K_w:
                    if self.hero.current_dir is None or self.hero.current_dir == 'down':
                        self.hero.current_dir = 'up'
                    elif self.hero.next_dir is None or self.hero.next_dir == 'down' or \
                            self.hero.current_dir == 'left' or self.hero.current_dir == 'right':
                        self.hero.next_dir = 'up'
                elif e.key == K_DOWN or e.key == K_s:
                    if self.hero.current_dir is None or self.hero.current_dir == 'up':
                        self.hero.current_dir = 'down'
                    elif self.hero.next_dir is None or self.hero.next_dir == 'up' or \
                            self.hero.current_dir == 'left' or self.hero.current_dir == 'right':
                        self.hero.next_dir = 'down'
                if e.key == K_i:
                    self.hero.lifes_count += 1
                if e.key == K_o:
                    self.hero.invincible = False if self.hero.invincible else True
                if e.key == K_p:
                    self.hero.endless_energy = False if self.hero.endless_energy else True
                    self.hero.energizer = False if self.hero.energizer else True
                if e.key == K_y:
                    menu.Game.save(self)
                if e.key == K_l:
                    self.sound_icon.change_mod(self)

        if len(self.dots) + len(self.energizers) == 0:
            self.won = True
        if self.hero.lifes_count <= 0:
            menu.Game.add_result(self)
            open('download.txt', 'w').close()
            pygame.time.wait(1000)
            menu.Game.end_game(self, False)
            raise SystemExit('YOU LOSE!!')

    def update(self):
        '''Обновляет поле и все сущности в нем'''
        self.screen.blit(self.bg, (0, 0))
        self.process_events(pygame.event.get())
        self.hero.update(self)
        self.check_energy()

        Life.print(self)
        self.score.print(self)
        Candy.update(self)
        for ghost in self.ghosts:
            ghost.update(self)
        self.entities.draw(self.screen)

    def check_energy(self):
        if self.hero.energizer:
            for ghost in self.ghosts:
                if not ghost.was_ate and not ghost.is_in_house:
                    ghost.scared = True
            if self.hero.endless_energy:
                self.get_ghosts_out()
        else:
            for ghost in self.ghosts:
                ghost.scared = ghost.was_ate = False
            self.get_ghosts_out()
            if self.timer.check_time():
                if self.timer.interval == 7:
                    self.timer = Timer(20)
                else:
                    self.timer = Timer(7)

    def init_ghosts(self):
        '''Инициализация приведений-монстров'''
        for ghost in self.ghosts:
            self.entities.remove(ghost)
        self.blinky = Ghost('blinky', self.gates[0], self.gates[1], self.win_width, self.win_height)
        self.blinky.is_in_house = False
        self.klyde = Ghost('klyde', self.gates[0] + SIZE, self.gates[1] + SIZE * 3, self.win_width, self.win_height)
        self.inky = Ghost('inky', self.gates[0], self.gates[1] + SIZE * 3, self.win_width, self.win_height)
        self.pinky = Ghost('pinky', self.gates[0] - SIZE, self.gates[1] + SIZE * 3, self.win_width, self.win_height)
        self.ghosts = {self.blinky, self.pinky, self.inky, self.klyde}
        for ghost in self.ghosts:
            self.entities.add(ghost)

    def get_ghosts_out(self):
        '''Выход приведений-монстров из домика'''
        if self.hero.eated_dots_count >= 30 and self.pinky.is_in_house:
            self.pinky.free(self.gates)
        if self.hero.eated_dots_count >= 60 and self.inky.is_in_house:
            self.inky.free(self.gates)
        if self.hero.eated_dots_count >= 90 and self.klyde.is_in_house:
            self.klyde.free(self.gates)
