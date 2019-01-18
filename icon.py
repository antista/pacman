from pygame import *
from const import SIZE, BACK_COLOR


class Icon(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface((SIZE, SIZE))
        self.image.fill(Color(BACK_COLOR))
        self.image.set_colorkey(Color(BACK_COLOR))
        self.rect = Rect(51, 20, SIZE, SIZE)
        self.active_image = image.load('images/sound.ico')
        self.image = self.active_image
        self.inactive_image = image.load('images/muted.ico')
        self.active = True

    def change_mod(self, field):
        field.entities.remove(self)
        if self.active:
            self.active = False
            self.image = self.inactive_image
            field.music_channel.set_volume(0.0)
        else:
            self.active = True
            self.image = self.active_image
            field.music_channel.set_volume(0.5)
        field.entities.add(self)
