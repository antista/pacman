import unittest
import pyautogui
import field as f
import game
import main
import menu as m
import entity as en
import pacman as pac
import ghost as g
import icon as i
import candy as c
import timer as t
import platforms as p
import dots as d
import lifes as l
import score as s
import pygame
from math import sqrt


class TestField(unittest.TestCase):
    def test_init_map(self):
        field = f.Field('tests/lvl1.txt')
        self.assertEqual(field.exits, [])
        self.assertEqual(field.gates, (232, -16))
        self.assertEqual(len(field.dots), 1)
        self.assertEqual(len(field.energizers), 0)
        self.assertEqual(len(field.platforms), 4)
        self.assertEqual((field.hero.rect.x, field.hero.rect.y), (160, 0))

    def test_init_exits(self):
        field = f.Field('tests/lvl2.txt')
        self.assertEqual(field.exits, [160, 224])
        self.assertEqual(len(field.dots), 0)
        self.assertEqual(len(field.platforms), 10)
        self.assertEqual((field.hero.rect.x, field.hero.rect.y), (192, 16))

    def test_init_energizers(self):
        field = f.Field('tests/lvl2.txt')
        self.assertEqual(len(field.energizers), 1)

    def test_init_candy(self):
        field = f.Field('tests/lvl3.txt')
        self.assertEqual(field.candy_coordinates, (176, 16))

    def test_check_energy(self):
        field = f.Field('levels/standart.txt')
        for ghost in field.ghosts:
            ghost.scared = ghost.was_ate = True
        field.timer = t.Timer(0)
        field.check_energy()
        for ghost in field.ghosts:
            self.assertFalse(ghost.scared)
            self.assertFalse(ghost.was_ate)
        self.assertEqual(field.timer.interval, 7)

        field.pinky.is_in_house = False
        field.hero.energizer = True
        field.hero.endless_energy = True
        field.update()
        self.assertTrue(field.blinky.scared)
        self.assertTrue(field.pinky.scared)
        self.assertFalse(field.inky.scared)
        self.assertFalse(field.klyde.scared)

    def test_get_ghosts_out(self):
        field = f.Field('levels/standart.txt')
        field.hero.eated_dots_count = 31
        field.get_ghosts_out()
        self.assertEqual(field.pinky.target, (field.gates[0], field.gates[1] - 32))
        field.hero.eated_dots_count = 61
        field.get_ghosts_out()
        self.assertEqual(field.inky.target, (field.gates[0], field.gates[1] - 32))
        field.hero.eated_dots_count = 91
        field.get_ghosts_out()
        self.assertEqual(field.klyde.target, (field.gates[0], field.gates[1] - 32))

    def test_keydown_events(self):
        field = f.Field('tests/lvl4.txt')
        self.assertEqual((field.hero.rect.x, field.hero.rect.y), (192, 32))
        pyautogui.press('up')
        # pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{'unicode': '', 'key': 273, 'mod': 0, 'scancode': 72}))
        # pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{'key':pygame.K_UP}))
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.next_dir, 'up')
        pyautogui.press('down')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.next_dir, 'down')
        pyautogui.press('right')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'right')
        pyautogui.press('left')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'left')

        field.hero.current_dir = None
        field.hero.next_dir = None
        pyautogui.press('up')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'up')
        pyautogui.press('down')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'down')
        self.assertEqual(field.hero.next_dir, None)

        field.hero.current_dir = None
        pyautogui.press('down')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'down')
        pyautogui.press('up')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'up')
        self.assertEqual(field.hero.next_dir, None)

        field.hero.current_dir = 'up'
        pyautogui.press('left')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.next_dir, 'left')

        field.hero.next_dir = None
        pyautogui.press('right')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.current_dir, 'up')
        self.assertEqual(field.hero.next_dir, 'right')

        self.assertEqual(field.hero.lifes_count, 3)
        pyautogui.press('i')
        field.process_events(pygame.event.get())
        self.assertEqual(field.hero.lifes_count, 4)

        self.assertFalse(field.hero.invincible)
        pyautogui.press('o')
        field.process_events(pygame.event.get())
        self.assertTrue(field.hero.invincible)
        pyautogui.press('o')
        field.process_events(pygame.event.get())
        self.assertFalse(field.hero.invincible)

        self.assertFalse(field.hero.energizer)
        self.assertFalse(field.hero.endless_energy)
        pyautogui.press('p')
        field.process_events(pygame.event.get())
        self.assertTrue(field.hero.energizer)
        self.assertTrue(field.hero.endless_energy)

        field.music_channel = field.music.play(loops=-1)
        self.assertTrue(field.sound_icon.active)
        pyautogui.press('l')
        field.process_events(pygame.event.get())
        self.assertFalse(field.sound_icon.active)

        open('download.txt', 'w').close()
        pyautogui.press('y')
        field.process_events(pygame.event.get())
        self.assertNotEqual(open('download.txt', 'r').read(1), '')

        self.assertFalse(field.won)
        field.dots, field.energizers = [], []
        field.process_events(pygame.event.get())
        self.assertTrue(field.won)

        with self.assertRaises(SystemExit) as cm:
            field.hero.lifes_count = -1
            field.process_events(pygame.event.get())

        the_exception = cm.exception
        self.assertEqual(the_exception.code, 'YOU LOSE!!')


class TestMain(unittest.TestCase):
    def test_process_events(self):
        menu = m.Menu()
        menu.draw_buttons()
        menu.show_buttons = True
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                             {'pos': (menu.records_button.x + 20, menu.records_button.y + 20)}))
        menu.process_events()
        self.assertFalse(menu.show_buttons)

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                             {'pos': (menu.back_button.x + 20, menu.back_button.y + 20)}))
        menu.process_events()
        self.assertTrue(menu.show_buttons)

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                             {'pos': (menu.help_button.x + 20, menu.help_button.y + 20)}))
        menu.process_events()
        self.assertFalse(menu.show_buttons)

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                             {'pos': (menu.cheats_button.x + 20, menu.cheats_button.y + 20)}))
        menu.process_events()
        self.assertFalse(menu.show_buttons)

        menu.show_buttons = True
        with self.assertRaises(SystemExit) as cm:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                                 {'pos': (menu.quit_button.x + 20, menu.quit_button.y + 20)}))
            menu.process_events()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 'GOODBYE!!!')

        menu = m.Menu()
        with self.assertRaises(SystemExit) as cm:
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
            menu.process_events()
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 'GOODBYE!!!')


class TestGame(unittest.TestCase):
    def test_load(self):
        file = open('download.txt', 'w')
        file.write('tests/lvl1.txt' + '\n')
        file.write('bay' + '\n')
        file.write('164' + ',' + '-2' + '\n')
        file.write('4' + '\n')
        file.write('10' + '\n')
        file.write('1' + '\n')
        for dot in f.Field('tests/lvl1.txt').dots:
            file.write(str(dot.rect.x) + ',' + str(dot.rect.y) + '\n')
        file.write('_\n')
        file.write('192,48' + '\n')
        file.write('_\n')
        file.close()
        field = game.Game.load()
        self.assertEqual(field.name_map, 'tests/lvl1.txt')
        self.assertEqual(field.player_name, 'bay')
        self.assertEqual((field.hero.rect.x, field.hero.rect.y), (164, -2))
        self.assertEqual(field.hero.lifes_count, 4)
        self.assertEqual(field.hero.eated_dots_count, 10)
        self.assertEqual(field.hero.energizer_eated, 1)
        self.assertEqual(len(field.dots), 1)
        self.assertEqual(len(field.energizers), 1)
        open('download.txt', 'w').close()


class TestIcon(unittest.TestCase):
    def test_change_mod(self):
        icon = i.Icon()
        field = f.Field('tests/lvl4.txt')
        field.music_channel = field.music.play()
        self.assertTrue(icon.active)
        self.assertEqual(icon.image, icon.active_image)
        icon.change_mod(field)
        self.assertFalse(icon.active)
        self.assertEqual(icon.image, icon.inactive_image)
        icon.change_mod(field)
        self.assertTrue(icon.active)
        self.assertEqual(icon.image, icon.active_image)


class TestCandy(unittest.TestCase):
    def test_init(self):
        candy = c.Candy(10, 10)
        self.assertEqual((candy.rect.x, candy.rect.y), (10, 10))

    def test_remove(self):
        field = f.Field('levels/standart.txt')
        self.assertIsNone(field.candy)
        field.candy = c.Candy(1, 1)
        self.assertIsNotNone(field.candy)
        field.candy.timer = t.Timer(0)
        field.candy.check_time(field)
        self.assertIsNone(field.candy)

    def test_update(self):
        field = f.Field('levels/standart.txt')
        c.Candy.update(field)
        self.assertIsNone(field.candy)
        field.hero.eated_dots_count = 70
        c.Candy.update(field)
        self.assertIsNotNone(field.candy)
        field.candy.timer = t.Timer(0)
        c.Candy.update(field)
        self.assertIsNone(field.candy)
        field.hero.eated_dots_count = 170
        c.Candy.update(field)
        self.assertIsNotNone(field.candy)
        field.hero.rect.x, field.hero.rect.y = field.candy_coordinates
        c.Candy.update(field)
        self.assertIsNone(field.candy)


class TestScore(unittest.TestCase):
    def test_get_score(self):
        field = f.Field('tests/lvl1.txt')
        field.hero.eated_dots_count = 10
        field.hero.energizer_eated = 6
        field.score.print(field)
        self.assertEqual(field.score.get(field), 400)


class TestEntities(unittest.TestCase):
    def test_move(self):
        e = en.Entity(50, 40, 10)
        e.update_move()
        self.assertEqual((e.rect.x, e.rect.y), (40, 40))
        e.current_dir = 'up'
        e.update_move()
        self.assertEqual((e.rect.x, e.rect.y), (40, 30))
        e.current_dir = 'right'
        e.update_move()
        self.assertEqual((e.rect.x, e.rect.y), (50, 30))
        e.current_dir = 'down'
        e.update_move()
        self.assertEqual((e.rect.x, e.rect.y), (50, 40))

    def test_exits(self):
        e = en.Entity(5, 30, 10)
        e.update_move()
        e.move_in_exits([0, 16])
        self.assertEqual((e.rect.x, e.rect.y), (20, 30))
        e.current_dir = 'right'
        e.update_move()
        e.move_in_exits([0, 16])
        self.assertEqual((e.rect.x, e.rect.y), (2, 30))


class TestPacman(unittest.TestCase):
    def test_collides(self):
        field = f.Field('tests/lvl4.txt')
        field.hero.next_dir = 'up'
        for i in range(9):
            field.hero.update_move()
            field.hero.collide(field)
        self.assertEqual(field.hero.eated_dots_count, 1)
        self.assertCountEqual(field.dots, {})
        self.assertCountEqual(field.energizers, {})
        self.assertTrue(field.hero.energizer)
        self.assertIsNone(field.hero.current_dir)
        self.assertIsNone(field.hero.next_dir)
        field.hero.current_dir = 'right'
        field.hero.update_move()
        field.hero.collide(field)
        field.hero.current_dir = 'left'
        field.hero.update_move()
        field.hero.collide(field)
        field.hero.current_dir = 'down'
        for i in range(9):
            field.hero.update_move()
            field.hero.collide(field)
        field.hero.current_dir = 'down'
        field.hero.next_dir = 'right'
        field.hero.update_move()
        field.hero.collide(field)
        self.assertEqual(field.hero.current_dir, 'right')

    def test_death(self):
        pacman = pac.Pacman(0, 0)
        pacman.energizer = True
        pacman.rect.x = pacman.rect.y = 16
        pacman.current_dir = 'up'
        pacman.dead(f.Field('tests/lvl1.txt'))
        self.assertFalse(pacman.energizer)
        self.assertEqual(pacman.current_dir, 'left')
        self.assertEqual(pacman.lifes_count, 2)
        self.assertEqual((pacman.rect.x, pacman.rect.y), (0, 0))

    def test_check_death(self):
        field = f.Field('levels/standart.txt')
        field.blinky.rect.x, field.blinky.rect.y = field.hero.rect.x, field.hero.rect.y
        field.hero.check_dead(field)
        self.assertEqual(field.hero.lifes_count, 2)
        field.blinky.rect.x, field.blinky.rect.y = field.hero.rect.x, field.hero.rect.y
        field.hero.energizer = True
        field.hero.check_dead(field)
        self.assertEqual(field.hero.lifes_count, 2)
        self.assertFalse(field.blinky.alive)
        field.blinky.alive = True
        field.blinky.was_ate = True
        field.hero.check_dead(field)
        self.assertEqual(field.hero.lifes_count, 1)

    def test_update(self):
        field = f.Field('tests/lvl1.txt')
        field.hero.energizer = True
        field.hero.timer = t.Timer(0)
        field.hero.update(field)
        self.assertFalse(field.hero.energizer)
        self.assertIsNone(field.hero.timer)


class TestLifes(unittest.TestCase):
    def test_init(self):
        life = l.Life(25, 60)
        life.draw(pygame.display.set_mode())
        self.assertEqual((life.rect.x, life.rect.y), (25, 60))
        l.Life.print(f.Field('tests/lvl1.txt'))


class TestGhosts(unittest.TestCase):
    def test_blinky(self):
        gh = g.Ghost('blinky', 10, 10, 20, 20)
        self.assertEqual(gh.target, (-124, -16))
        gh.target = (-100000, -100000000)
        field = f.Field('tests/lvl1.txt')
        gh.change_target(field, 7)
        self.assertEqual(gh.target, gh.default_target)
        gh.change_target(field, 0)
        self.assertEqual(gh.target, (field.hero.rect.x, field.hero.rect.y))

    def test_pinky(self):
        gh = g.Ghost('pinky', 10, 10, 20, 20)
        self.assertEqual(gh.target, (176, -16))
        gh.is_in_house = False
        gh.target = (-100000, -100000000)
        field = f.Field('tests/lvl1.txt')
        gh.change_target(field, 7)
        self.assertEqual(gh.target, gh.default_target)
        gh.change_target(field, 0)
        self.assertEqual(gh.target, (field.hero.rect.x + field.hero.xvel * 2, field.hero.rect.y + field.hero.yvel * 2))

    def test_inky(self):
        gh = g.Ghost('inky', 10, 10, 20, 20)
        self.assertEqual(gh.target, (-124, 36))
        gh.is_in_house = False
        gh.target = (-100000, -100000000)
        field = f.Field('tests/lvl1.txt')
        gh.change_target(field, 7)
        self.assertEqual(gh.target, gh.default_target)
        gh.change_target(field, 0)
        self.assertEqual(gh.target, (
            field.blinky.rect.x + (field.hero.rect.x + field.hero.xvel / 2 * 16 - field.blinky.rect.x) * 2,
            field.blinky.rect.y + (field.hero.rect.y + field.hero.yvel / 2 * 16 - field.blinky.rect.y) * 2))

    def test_klyde(self):
        gh = g.Ghost('klyde', 10, 10, 20, 20)
        self.assertEqual(gh.target, (176, 36))
        gh.is_in_house = False
        gh.target = (-100000, -100000000)
        field = f.Field('tests/lvl1.txt')
        gh.change_target(field, 7)
        self.assertEqual(gh.target, gh.default_target)
        gh.change_target(field, 0)
        self.assertEqual(gh.target, (field.hero.rect.x, field.hero.rect.y) if sqrt(
            (gh.rect.x - field.hero.rect.x) * (gh.rect.x - field.hero.rect.x) +
            (gh.rect.y - field.hero.rect.y) * (gh.rect.y - field.hero.rect.y)) > 8 * 16 else gh.default_target)

    def test_decision_not_collide(self):
        gh = g.Ghost('blinky', 10, 10, 20, 20)
        gh.target = (5, -5)
        gh.decide_direction([p.Platform(-20, -20)])
        self.assertEqual(gh.current_dir, 'up')

    def test_decision_collide(self):
        gh = g.Ghost('blinky', 16, 16)
        gh.target = (32, -16)
        gh.current_dir = 'down'
        gh.decide_direction([p.Platform(16, 0)])
        self.assertEqual(gh.current_dir, 'right')

    def test_free(self):
        gh = g.Ghost('blinky', 16, 16)
        gates = (16, 0)
        gh.free(gates)
        self.assertEqual(gh.target, (16, -32))
        for i in range(8):
            gh.decide_direction([])
            gh.update_move()
            gh.free(gates)
        self.assertEqual(gh.target, gh.default_target)

    def test_scare(self):
        gh = g.Ghost('blinky', 16, 16)
        gh.target = (0, 0)
        self.assertEqual(gh.target, (0, 0))
        gh.scared = True
        gh.update(f.Field('tests/lvl1.txt'))
        self.assertTrue(gh.scared)
        self.assertNotEqual(gh.target, (0, 0))
        gh.alive = False
        gh.rect.x = gh.rect.y = 16
        gh.update(f.Field('tests/lvl1.txt'))
        self.assertFalse(gh.scared)

    def test_update(self):
        gh = g.Ghost('blinky', 16, 16)
        gh.image = None
        gh.update(f.Field('tests/lvl1.txt'))
        self.assertEqual(gh.image, gh.default_image)


class TestTimer(unittest.TestCase):
    def test_timer(self):
        self.assertFalse(t.Timer(10).check_time())
        self.assertTrue(t.Timer(0).check_time())


class TestPlatforms(unittest.TestCase):
    def test_platform(self):
        platform = p.Platform(0, 0)
        self.assertEqual((platform.rect.x, platform.rect.y), (0, 0))

    def test_gates(self):
        gate = p.Gate(10, 10)
        self.assertEqual((gate.rect.x, gate.rect.y), (10, 10))


class TestDots(unittest.TestCase):
    def test_dot(self):
        dot = d.Dot(5, 6)
        self.assertEqual((dot.rect.x, dot.rect.y), (5, 6))

    def test_energizer(self):
        energizer = d.Energizer(40, 45)
        self.assertEqual((energizer.rect.x, energizer.rect.y), (40, 45))


if __name__ == '__main__':
    unittest.main()
