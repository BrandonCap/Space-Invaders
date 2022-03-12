import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint


# from alien import Alien
# from stats import Stats


class Lasers:
    def __init__(self, game):
        self.game = game
        self.stats = game.stats
        self.alien_fleet = game.alien_fleet
        self.ufo = game.ufo
        self.lasers = Group()

    def add(self, laser):
        self.lasers.add(laser)

    def empty(self):
        self.lasers.empty()

    def fire(self):
        new_laser = Laser(self.game)
        self.lasers.add(new_laser)
        bulletSound = pg.mixer.Sound('Sounds/shoot.wav')
        bulletSound.play()

    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)

        collisions_fleet = pg.sprite.groupcollide(self.alien_fleet.fleet, self.lasers, False, True)
        for alien in collisions_fleet:
            if not alien.dying:
                alien.hit()
                deathSound = pg.mixer.Sound('Sounds/invaderkilled.wav')
                deathSound.play()
        collisions_ufo = pg.sprite.groupcollide(self.ufo.fleet, self.lasers, False, True)
        for ufo in collisions_ufo:
            if not ufo.dying:
                ufo.ufo_hit()
                deathSound = pg.mixer.Sound('Sounds/invaderkilled.wav')
                deathSound.play()

        if self.alien_fleet.length() == 0:
            self.stats.level_up()
            self.game.restart()

        for laser in self.lasers:
            laser.update()

    def draw(self):
        for laser in self.lasers:
            laser.draw()


class Laser(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship

        self.rect = pg.Rect(0, 0, self.w, self.h)
        self.center = copy(self.ship.center)
        # print(f'center is at {self.center}')
        # self.color = self.settings.laser_color
        tu = 50, 255
        self.color = randint(*tu), randint(*tu), randint(*tu)
        self.v = Vector(0, -1) * self.settings.laser_speed_factor

    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self): pg.draw.rect(self.screen, color=self.color, rect=self.rect)
