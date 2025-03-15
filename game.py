import pygame as pg
import helpers
from classes import *


class Game:
    def __init__(self, render_image: pg.Surface, screen: pg.Surface, window_size: (int, int)):
        self.render_image = render_image
        self.screen = screen
        self.window_size = window_size
        self.bodies = []
        self.mouse_down = False
        self.mouse_mov = pg.Vector2(0, 0)
        self.start_traj_pos = (self.window_size[0] / 2, self.window_size[1] / 2)
        self.traj_color = (0, 255, 0)


    def update(self):
        draw_area = pg.Rect(0, 0, self.window_size[0], self.window_size[1])
        cropped_surface = pg.Surface((self.window_size[0], self.window_size[1]))
        # blit onto the cropped size surface and scale it up to the window size
        cropped_surface.blit(self.render_image, (0, 0), draw_area)
        self.screen.blit(cropped_surface, (0, 0))
        self.render_image.fill((0, 0, 0))  # paint sreen black before re-drawing objects

        self.update_bodies()
        # pg.event.pump()
        # pg.display.flip()  # updates the entire surface
        self.draw_trajectory()
        pg.display.update()

    def draw_trajectory(self):
        pg.draw.line(self.render_image, self.traj_color, self.start_traj_pos,
                     self.start_traj_pos + self.mouse_mov)

    def render_circle(self, body: Body):
        # circle = helpers.get_points_in_circle(body.cx, body.cy, body.radius)
        pg.draw.circle(self.render_image, body.color, (body.cx, body.cy), body.radius)
        # [self.render_image.set_at((pt[0], pt[1]), body.color) for pt in circle]

    def update_bodies(self):
        for body in self.bodies:
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

