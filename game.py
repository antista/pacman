import field as fid
from field import *
from icon import *


class Game:
    @staticmethod
    def start_game(field):
        '''Основной метод, отвечающий за работу и завершение игры'''
        timer = pygame.time.Clock()
        levels = {'big_map', 'big_map1', 'small', 'almost_stand', 'long'}
        pygame.init()
        pygame.mixer.init()
        field.music_channel = field.music.play(loops=-1)
        field.music_channel.set_volume(0.5)

        while field.active:
            timer.tick(25)
            field.update()
            pygame.display.update()

            if field.won:
                field.music_channel.set_volume(0.0)
                pygame.mixer.Sound('sounds/end_lvl.wav').play()
                current_score = field.score.get(field)
                current_lifes_count = field.hero.lifes_count
                pygame.time.wait(6000)
                if levels != set():
                    sound = field.sound_icon
                    field = fid.Field('levels/' + levels.pop() + '.txt', current_score, current_lifes_count)
                    field.music_channel = field.music.play(loops=-1)
                    field.music_channel.set_volume(0.5)
                    if not sound.active:
                        field.sound_icon.change_mod(field)
                else:
                    Game.add_result(field)
                    Game.end_game(field, True)
                    raise SystemExit('YOU WON!!!')

    @staticmethod
    def ask_for_save(field):
        '''Выводит на экран вопрос о сохранении игры'''
        pygame.init()
        while True:
            pygame.draw.rect(field.screen, Color('#888888'),
                             (field.win_width / 2 - 250, field.win_height / 2 - 150, 500, 300))
            field.screen.blit(pygame.font.Font(None, 100).render("Save game?", True, pygame.Color("Darkblue")),
                              (field.win_width / 2 - 200, field.win_height / 2 - 80))

            yes_button = pygame.draw.rect(field.screen, Color('Green'),
                                          (field.win_width / 2 - 200, field.win_height / 2 + 50, 150, 50))
            field.screen.blit(pygame.font.Font(None, 50).render("Yes", True, pygame.Color("White")),
                              (field.win_width / 2 - 160, field.win_height / 2 + 60))

            no_button = pygame.draw.rect(field.screen, Color('Darkred'),
                                         (field.win_width / 2 + 50, field.win_height / 2 + 50, 150, 50))
            field.screen.blit(pygame.font.Font(None, 50).render("No", True, pygame.Color("White")),
                              (field.win_width / 2 + 100, field.win_height / 2 + 60))

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.time.wait(500)
                    if yes_button.collidepoint(pygame.mouse.get_pos()):
                        Game.save(field)
                        return
                    if no_button.collidepoint(pygame.mouse.get_pos()):
                        open('download.txt', 'w').close()
                        return
            pygame.display.flip()

    @staticmethod
    def save(field):
        '''Сохраняет игру в файл download.txt'''
        f = open('download.txt', 'w')
        f.write(field.name_map + '\n')
        f.write(field.player_name + '\n')
        f.write(str(field.hero.rect.x) + ',' + str(field.hero.rect.y) + '\n')
        f.write(str(field.hero.lifes_count) + '\n')
        f.write(str(field.hero.eated_dots_count) + '\n')
        f.write(str(field.hero.energizer_eated) + '\n')
        for dot in field.dots:
            f.write(str(dot.rect.x) + ',' + str(dot.rect.y) + '\n')
        f.write('_\n')
        for energizer in field.energizers:
            f.write(str(energizer.rect.x) + ',' + str(energizer.rect.y) + '\n')
        f.write('_\n')
        f.close()

    @staticmethod
    def load():
        '''Загружает игру из файла download.txt'''
        f = open('download.txt')
        field = fid.Field(f.readline()[:-1])
        field.player_name = f.readline()[:-1]
        tmp = f.readline()[:-1].split(',')
        field.hero.rect.x, field.hero.rect.y = int(tmp[0]), int(tmp[1])
        field.hero.lifes_count = int(f.readline()[:-1])
        field.hero.eated_dots_count = int(f.readline()[:-1])
        field.hero.energizer_eated = int(f.readline()[:-1])
        field.entities.remove(field.dots)
        field.entities.remove(field.energizers)
        field.dots = pygame.sprite.Group()
        field.energizers = pygame.sprite.Group()
        while True:
            tmp = f.readline()[:-1]
            if tmp == '_':
                break
            tmp = tmp.split(',')
            d = Dot(int(tmp[0]), int(tmp[1]))
            field.dots.add(d)
            field.entities.add(d)
        while True:
            tmp = f.readline()[:-1]
            if tmp == '_':
                break
            tmp = tmp.split(',')
            e = Energizer(int(tmp[0]), int(tmp[1]))
            field.energizers.add(e)
            field.entities.add(e)

        f.close()
        for ghost in field.ghosts:
            field.entities.remove(ghost)
            field.entities.add(ghost)
        return field

    @staticmethod
    def add_result(field):
        '''Добавление результата в таблицу рекордов'''
        f = open('records.txt')
        records = []
        current_score = field.score.get(field)
        for record in f:
            records.append(record[:-1])
        for i in range(len(records)):
            if current_score > int(records[i].split('/')[1]):
                if len(records) < 10:
                    records.append(records[-1])
                for j in range(len(records) - 1, i, -1):
                    records[j] = records[j - 1]
                records[i] = field.player_name + '/' + str(current_score)
                break
        else:
            if len(records) < 10:
                records.append(field.player_name + '/' + str(current_score))
        f.close()
        f = open('records.txt', 'w')
        for record in records:
            f.write(str(record) + '\n')
        f.close()

    @staticmethod
    def end_game(field, is_won):
        pygame.init()
        pygame.mixer.Sound('sounds/death.wav').play()
        text_surface = pygame.font.SysFont("comicsansms", 100).render("YOU WON!" if is_won else "YOU LOSE!", True,
                                                                      Color("green") if is_won else Color('red'))
        field.screen.blit(text_surface, (
            (field.win_width - text_surface.get_width()) / 2,
            (field.win_height - text_surface.get_height()) / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
