import pygame
from pygame import *
import field
# from field import *
import time
from game import Game

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50


class Menu():
    def __init__(self):
        '''Инициализирует меню игры и запускает его'''
        self.active = True
        self.field = field.Field('levels/standart.txt')
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.sound_effect = pygame.mixer.Sound('sounds/enter.wav')

    def run(self):
        '''Метод с основным циклом меню'''
        self.show_buttons = True
        while self.active:
            if self.show_buttons:
                self.draw_buttons()
            self.process_events()

    def process_events(self):
        '''Обрабатывает события нажатия на кнопки меню'''
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit('GOODBYE!!!')
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pygame.mixer.Sound('sounds/enter.wav').play()
                    pygame.time.wait(1000)
                    self.active = False
                    open('download.txt', 'w').close()
                    self.get_player_name()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    pygame.mixer.Sound('sounds/enter.wav').play()
                    pygame.time.wait(1000)
                    self.active = False
                    open('download.txt', 'w').close()
                    self.get_player_name()

                if self.continue_button.collidepoint(event.pos):
                    if open('download.txt', 'r').read(1) != '':
                        self.sound_effect.play()
                        pygame.time.wait(1000)
                        self.field = Game.load()
                        Game.start_game(self.field)

                if self.records_button.collidepoint(event.pos):
                    self.sound_effect.play()
                    pygame.time.wait(1000)
                    self.show_buttons = False
                    self.show_records()

                if self.help_button.collidepoint(event.pos):
                    self.sound_effect.play()
                    pygame.time.wait(1000)
                    self.show_buttons = False
                    self.show_help()

                if self.quit_button.collidepoint(event.pos):
                    self.sound_effect.play()
                    pygame.time.wait(1000)
                    raise SystemExit('GOODBYE!!!')

                if self.back_button is not None and self.back_button.collidepoint(event.pos):
                    self.sound_effect.play()
                    pygame.time.wait(1000)
                    self.show_buttons = True
                    self.field.screen.fill(Color('Black'))

                if self.cheats_button is not None and self.cheats_button.collidepoint(event.pos):
                    self.sound_effect.play()
                    pygame.time.wait(1000)
                    self.show_text('cheats.txt')

        pygame.display.flip()

    def draw_text_on_button(self, button, text):
        '''Добавляет текст на кнопку'''
        font = pygame.font.Font(None, int(button.height / 1.3))
        text_surface = font.render(text, True, Color("White"))
        self.field.screen.blit(text_surface, (
            (button.x + button.width / 2) - text_surface.get_width() / 2,
            (button.y + button.height / 2) - text_surface.get_height() / 2))

    def draw_buttons(self):
        '''Отображает все кнопки меню на экране'''
        button = (self.field.win_width / 2, self.field.win_height / 5 - 30)
        left_up_dot = (self.field.win_width - button[0]) / 2

        self.start_button = pygame.draw.rect(self.field.screen, Color('limegreen'),
                                             (left_up_dot, button[1] / 2, *button))
        self.draw_text_on_button(self.start_button, "Start game")

        self.continue_button = pygame.draw.rect(self.field.screen,
                                                Color('Orange') if open('download.txt', 'r').read(1) != ''
                                                else Color('#525252'), (left_up_dot, 1.75 * button[1], *button))
        self.draw_text_on_button(self.continue_button, "Continue")

        self.records_button = pygame.draw.rect(self.field.screen, Color('Blue'),
                                               (left_up_dot, 3 * button[1], *button))
        self.draw_text_on_button(self.records_button, "Records")

        self.help_button = pygame.draw.rect(self.field.screen, Color('Purple'),
                                            (left_up_dot, 4.25 * button[1], *button))
        self.draw_text_on_button(self.help_button, "Help")

        self.quit_button = pygame.draw.rect(self.field.screen, Color('Darkred'),
                                            (left_up_dot, 5.5 * button[1], *button))
        self.draw_text_on_button(self.quit_button, "Exit")

        self.back_button = None
        self.cheats_button = None

    def show_records(self):
        '''Выводит рекорды на экран'''
        self.field.screen.fill(Color('Black'))
        f = open('records.txt')
        x, y = self.field.win_width / 5, 30
        font = pygame.font.Font(None, 30)
        for record in f:
            text = font.render(
                record.split('/')[0] + ' ' + ' ' * (7 - int(len(record) / 2)) + '.' * (65 - len(record)) + '  ' +
                record.split('/')[1][:-1], True, pygame.Color("#999999"))
            self.field.screen.blit(text, [x, y])
            y += 40
        f.close()
        self.back_button = pygame.draw.rect(self.field.screen, Color('Blue'), (
            self.field.win_width - BUTTON_WIDTH / 1.5, self.field.win_height - 1.5 * BUTTON_HEIGHT, BUTTON_WIDTH / 2,
            BUTTON_HEIGHT))
        self.draw_text_on_button(self.back_button, "Back")

    def show_text(self, file):
        '''Выводит текст на экран'''
        self.field.screen.fill(Color('Black'))
        f = open(file)
        x, y = self.field.win_width / 10, 30
        font = pygame.font.Font(None, 35)
        for line in f:
            text = font.render(line[:-1], True, pygame.Color("#999999"))
            self.field.screen.blit(text, [x, y])
            y += 40
        f.close()
        self.back_button = pygame.draw.rect(self.field.screen, Color('Blue'), (
            self.field.win_width - BUTTON_WIDTH / 1.2, self.field.win_height - 1.5 * BUTTON_HEIGHT, BUTTON_WIDTH / 1.5,
            BUTTON_HEIGHT / 1.2))
        self.draw_text_on_button(self.back_button, "Back")

    def show_help(self):
        '''Выводит помощь на экран'''
        self.show_text('help.txt')
        self.cheats_button = pygame.draw.rect(self.field.screen, Color('#7E2A8D'), (
            self.field.win_width - BUTTON_WIDTH / 1.2, self.field.win_height - 2.7 * BUTTON_HEIGHT, BUTTON_WIDTH / 1.5,
            BUTTON_HEIGHT / 1.2))
        self.draw_text_on_button(self.cheats_button, "Cheats")

    def get_player_name(self):
        '''Получает имя игрока через отображающуюся форму'''
        input_font = pygame.font.Font(None, 45)
        invite_font = pygame.font.Font(None, 100)
        input_box = Rect(self.field.win_width / 2 - 150, self.field.win_height / 2 + 50, 300, 50)
        text = ''
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if text != '':
                            self.field.player_name = text
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 15:
                        text += event.unicode

            self.field.screen.fill(Color('Black'))
            self.field.screen.blit(input_font.render(text, True, Color('White')), (input_box.x + 10, input_box.y + 10))
            self.field.screen.blit(invite_font.render('Enter the name', True, Color('White')),
                                   (self.field.win_width / 5.5, self.field.win_height / 4))
            self.field.screen.blit(pygame.font.Font(None, 25).render('( press \'Enter\' )', True, Color('#999999')),
                                   (input_box.x + 85, input_box.y + 65))
            pygame.draw.rect(self.field.screen, Color('lightskyblue3'), input_box, 2)
            pygame.display.flip()
        else:
            time.sleep(1)
            Game.start_game(self.field)
