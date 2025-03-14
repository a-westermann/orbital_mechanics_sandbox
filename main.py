import pygame as pg
from pygame.locals import *
from pygame import time
import gc


def main():
    pg.init()
    window_size = [2560, 1440]
    flags = FULLSCREEN | DOUBLEBUF
    screen = pg.display.set_mode(window_size)
    gc.disable()  # disable gc worth it?
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])  # limit allowed events we have to check for every frame
    clock = time.Clock()
    game_running = True

    while game_running:
        clock.tick(60)  # fps limit
        fps = clock.get_fps()
        print(f'fps: {str(round(fps))}')

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game_running = False

    pg.quit()


main()
