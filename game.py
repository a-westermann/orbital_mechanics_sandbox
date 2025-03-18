import pygame as pg
import helpers
from classes import *
import level_builder
import math


class Game:
    def __init__(self, render_image: pg.Surface, screen: pg.Surface, window_size: (int, int)):
        self.render_image = render_image
        self.screen = screen
        self.window_size = window_size
        self.level = 3
        self.current_level: Level = None
        self.bodies : [Body] = []
        self.mouse_down = False
        self.mouse_mov = pg.Vector2(0, 0)
        self.mouse_mov_multi = 0.02
        self.start_traj_pos = (self.window_size[0] / 2, self.window_size[1] / 2)
        self.traj_color = (0, 255, 0)
        self.comet_moving = False  # used to stop comet from being gravitied before shooting
        self.goal : Goal = None
        self.nogoZones : [NoGoZone] = []
        self.wormhole_cd = 0
        pg.font.init()


    def setup_level(self):
        self.mouse_mov = pg.Vector2(0, 0)
        self.current_level = level_builder.load_level(self.level)
        self.bodies = self.current_level.bodies
        self.goal = self.current_level.goal
        self.nogoZones = self.current_level.nogos
        self.wormholes = self.current_level.wormholes
        self.comet_moving = False
        font = pg.font.SysFont('Calibri', 26)
        self.text_surface = font.render(self.current_level.name, False, (255, 255, 255))



    def update(self):
        draw_area = pg.Rect(0, 0, self.window_size[0], self.window_size[1])
        cropped_surface = pg.Surface((self.window_size[0], self.window_size[1]))
        # blit onto the cropped size surface and scale it up to the window size
        cropped_surface.blit(self.render_image, (0, 0), draw_area)
        self.screen.blit(cropped_surface, (0, 0))
        self.render_image.fill((0, 0, 0))  # paint sreen black before re-drawing objects
        self.render_image.blit(self.text_surface, (0, 0))

        self.update_bodies()
        # pg.event.pump()
        # pg.display.flip()  # updates the entire surface
        self.draw_trajectory()
        pg.draw.rect(self.render_image, self.goal.color, self.goal)  # draw the goal
        for nogo in self.nogoZones:
            self.lerp_color(nogo)
            pg.draw.rect(self.render_image, nogo.color, nogo)

        for wormhole in self.wormholes:
            pg.draw.rect(self.render_image, wormhole.color, wormhole)
        self.wormhole_cd += 1
        if self.wormhole_cd > 20:
            wormhole_index = self.check_wormhole_collision()
            if wormhole_index != -1:
                self.wormhole_cd = 0
                self.enter_wormhole(wormhole_index)

        # anything past here will affect the following level!
        if self.check_goal_collision():
            self.next_level()
        if self.check_nogo_collision():
            self.setup_level()
            return

        pg.display.update()



    def check_wormhole_collision(self):
        for i, w in enumerate(self.wormholes):
            if w.collidepoint((self.bodies[0].cx, self.bodies[0].cy)):
                return i
        return -1

    def enter_wormhole(self, hole_index):
        enter_hole_a = hole_index % 2 == 0
        hole_enter = self.wormholes[hole_index]
        hole_exit = self.wormholes[hole_index + 1] if enter_hole_a else self.wormholes[hole_index - 1]
        self.bodies[0].cx, self.bodies[0].cy = hole_exit.centerx, hole_exit.centery


    def check_nogo_collision(self):
        for n in self.nogoZones:
            if n.collidepoint((self.bodies[0].cx, self.bodies[0].cy)):
                return True
        return False

    def check_goal_collision(self) -> bool:
        return self.goal.collidepoint((self.bodies[0].cx, self.bodies[0].cy))

    def next_level(self):
        self.level += 1
        self.setup_level()

    def draw_trajectory(self):
        pg.draw.line(self.render_image, self.traj_color, self.start_traj_pos,
                     self.start_traj_pos + self.mouse_mov)

    def render_circle(self, body: Body):
        # circle = helpers.get_points_in_circle(body.cx, body.cy, body.radius)
        pg.draw.circle(self.render_image, body.color, (body.cx, body.cy), body.radius)
        # [self.render_image.set_at((pt[0], pt[1]), body.color) for pt in circle]

    def update_comet(self):
        if self.comet_moving:
            self.bodies[0].velocity += -self.mouse_mov * self.mouse_mov_multi
            self.mouse_mov = pg.Vector2(0, 0)


    def update_bodies(self):
        for body in self.bodies:
            if body.comet and not self.comet_moving:
                self.render_circle(body)
                continue  # don't allow comet to move until shot

            if body.static:
                self.render_circle(body)
                continue  # don't allow gravity to affect this body
            # get updated position
            other_bodies = self.get_other_bodie(body.cx, body.cy)
            # body.color = (255, 0, 0) if other_bodies else body.default_color  # testing
            destroyed = False
            for other in other_bodies:
                if destroyed:
                    continue
                dist = max(1, helpers.get_dist(body.cx, other.cx, body.cy, other.cy))
                if dist < other.radius and other.radius > body.radius:
                    destroyed = True
                    if body.comet:  # comet was destroyed
                        self.setup_level()
                        return
                    self.bodies.remove(body)
                    continue
                grav_accel = helpers.get_grav_accel(body, other, dist)
                body.velocity = (body.velocity[0] + (other.cx - body.cx) * grav_accel,
                                 body.velocity[1] + (other.cy - body.cy) * grav_accel)
            body.cx, body.cy = body.cx + body.velocity[0], body.cy + body.velocity[1]
            self.render_circle(body)

    def get_other_bodie(self, cx: int, cy: int) -> [Body]:
        others = []
        for body in self.bodies:
            if body.cx == cx and body.cy == cy:
                continue
            if abs(body.cx - cx) + abs(body.cy - cy) < body.soi:
                others.append(body)

        return others


    def lerp_color(self, obj: ColorLerpObject):
        obj.update_color()
