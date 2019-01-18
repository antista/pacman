#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from menu import *


def main():
    # pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.display.set_caption("Pacman")
    pygame.display.set_icon(image.load('images/pacman32.png'))

    menu = Menu()
    menu.run()


if __name__ == "__main__":
    main()
