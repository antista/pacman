import pygame

SCORE = 0


class Score():
    def __init__(self, last_score):
        self.points = last_score

    def get(self, field):
        '''Возвращает количество очков счета'''
        return field.hero.eated_dots_count * 10 + field.hero.energizer_eated * 50 + self.points

    def print(self, field):
        '''Отображает счет на экране'''
        pygame.init()
        font = pygame.font.Font(None, 30)
        text = font.render("SCORE: " + str(self.get(field)), True, pygame.Color("#999999"))
        field.screen.blit(text, [15, field.win_height - 50])
