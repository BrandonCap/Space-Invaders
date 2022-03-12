import pygame as pg

import landing_page
from landing_page import LandingPage
from sys import exit
import game_functions as gf
from time import sleep
from stats import Stats
from scoreboard import Scoreboard
from laser import Lasers
from ship import Ship
from alien import AlienFleet
from alien import UFO
from settings import Settings

bg_img = pg.image.load(f'images/background.jpeg')
bg_img = pg.transform.scale(bg_img, (1200, 800))

class Game:
    RED = (255, 0, 0)


    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.sb = Scoreboard(game=self)
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.ufo = UFO(game=self)
        self.lasers = Lasers(game=self)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)
        #self.alien_fleet.set_lasers(self.lasers)

    def restart(self):
        if self.stats.ships_left == 0: 
          self.game_over()
        print("restarting game")
        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ufo.empty()
        self.ufo.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.ufo.update()
        self.lasers.update()
        self.sb.update()

    def draw(self):
        self.screen.blit(bg_img, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.ufo.draw()
        self.lasers.draw()
        self.sb.draw()
        pg.display.flip()

    def play(self):
        self.finished = False

        #pg.mixer.init()
        pg.mixer.music.load(landing_page.playlist.pop())
        pg.mixer.music.play()

        while not self.finished:
            self.update()
            self.draw()
            gf.check_events(game=self)   # exits game if QUIT pressed
        self.game_over()

    def game_over(self): 
      print('\nGAME OVER!\n\n')  
      exit()    # can ask to replay here instead of exiting the game

def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()
    # pg.mixer.init()
    # pg.mixer.music.load('Sounds/12_Invader Homeworld.mp3')
    # pg.mixer.music.play()


if __name__ == '__main__':
    main()
