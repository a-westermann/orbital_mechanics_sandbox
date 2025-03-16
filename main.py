import math
import random

import pygame as pg
from pygame.locals import *
from pygame import time
import gc
# import numpy as np
from game import Game
from classes import *


def main():
    pg.init()
    window_size = [1920 , 1080]  # [2560, 1440]  # [1920 , 1080]
    flags = FULLSCREEN | DOUBLEBUF
    screen = pg.display.set_mode(window_size)
    gc.disable()  # disable gc worth it?
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])  # limit allowed events we have to check for every frame
    clock = time.Clock()

    surface = pg.Surface((window_size[0], window_size[1]))
    game = Game(surface, screen, window_size)

    game_running = True

    game.setup_level()
    # testing
    # game.bodies.append(Body(100, 600, 4, (0, 0), (0, 255, 255)))
    # game.bodies.append(Body(150, 850, 8, (2, 2), (255, 255, 0)))
    # game.bodies.append(Body(1200, 600, 80, (0, 0), (255, 255, 255)))
    # game.bodies.append(Body(1650, 400, 2, (-3, -2.5), (255, 0, 255)))
    # for i in range(random.randrange(200, 250)):
    #     x, y = random.randrange(0, window_size[0]), random.randrange(0, window_size[1])
    #     size = random.randrange(1, 10)
    #     max_vel = 7
    #     vx, vy = random.randrange(-max_vel, max_vel), random.randrange(-max_vel, max_vel)
    #     color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    #     game.bodies.append(Body(x, y, size, (vx, vy), color))


    while game_running:
        clock.tick(120)  # fps limit
        fps = clock.get_fps()
        # print(f'fps: {str(round(fps))}')

        events = pg.event.get()
        for event in events:
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and keys[pg.K_ESCAPE]):
                game_running = False

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                game.mouse_down = True
                game.mouse_mov.update((0, 0))
                pg.mouse.set_visible(False)
            elif game.mouse_down and event.type == pg.MOUSEBUTTONUP and not pg.mouse.get_pressed()[0]:
                game.mouse_down = False
                game.shoot_comet = True
                pg.mouse.set_visible(True)

            if game.mouse_down and event.type == pg.MOUSEMOTION:
                traj_vector = pg.Vector2(event.rel)
                max_len = 250
                if (game.mouse_mov[0] * traj_vector[0] > 0) and abs(game.mouse_mov[0]) > max_len:
                    traj_vector = (0, traj_vector[1])
                if (game.mouse_mov[1] * traj_vector[1] > 0) and abs(game.mouse_mov[1]) > max_len:
                    traj_vector = (traj_vector[0], 0)
                game.mouse_mov += traj_vector

            if pg.KEYDOWN and keys[pg.K_SPACE]:
                game.setup_level()


        game.update_comet()
        game.update()

    pg.quit()


main()
