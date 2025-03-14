import pygame as pg
from pygame.locals import *
from pygame import time
import gc
import numpy as np
from game import Game


def main():
    pg.init()
    window_size = [1920 , 1080]  # [2560, 1440]
    flags = FULLSCREEN | DOUBLEBUF
    screen = pg.display.set_mode(window_size)
    gc.disable()  # disable gc worth it?
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])  # limit allowed events we have to check for every frame
    clock = time.Clock()

    surface = pg.Surface((window_size[0], window_size[1]))
    game = Game(surface, screen, window_size)

    game_running = True

    while game_running:
        clock.tick(60)  # fps limit
        fps = clock.get_fps()
        print(f'fps: {str(round(fps))}')

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                game_running = False

        game.render_circle(90, 90, 20)
        game.update()

    pg.quit()


main()
