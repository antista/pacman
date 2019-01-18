from pygame import *
from const import SIZE, BACK_COLOR
from timer import Timer
from score import Score
from random import randint

candies = ['apple', 'cherry', 'grape', 'peach', 'strawberry']


class Candy(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, SIZE, SIZE)
        self.image = Surface((SIZE, SIZE))
        self.image.fill(Color(BACK_COLOR))
        self.image.set_colorkey(Color(BACK_COLOR))
        self.image = image.load('images/candies/' + candies[randint(0, 4)] + '.ico')
        self.timer = None

    def check_time(self, field):
        if self.timer.check_time():
            field.entities.remove(self)
            field.candy = None

    @staticmethod
    def update(field):
        if field.hero.eated_dots_count == 70 or field.hero.eated_dots_count == 170:
            if field.candy is None:
                field.candy = Candy(*field.candy_coordinates)
                field.entities.add(field.candy)
                field.candy.timer = Timer(9)
        if field.candy is not None:
            if sprite.collide_rect(field.hero, field.candy):
                mixer.Sound('sounds/eat_fruit.wav').play()
                field.entities.remove(field.candy)
                field.candy = None
                field.score = Score(field.score.points + 500)
            if field.candy is not None:
                field.candy.check_time(field)
