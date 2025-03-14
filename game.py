import pygame as pg
import helpers


class Game:
    def __init__(self, render_image: pg.Surface, screen: pg.Surface, window_size: (int, int)):
        self.render_image = render_image
        self.screen = screen
        self.window_size = window_size

    def update(self):
        draw_area = pg.Rect(0, 0, self.window_size[0], self.window_size[1])
        cropped_surface = pg.Surface((self.window_size[0], self.window_size[1]))
        # blit onto the cropped size surface and scale it up to the window size
        cropped_surface.blit(self.render_image, (0, 0), draw_area)
        self.screen.blit(cropped_surface, (0, 0))
        pg.event.pump()
        pg.display.flip()  # updates the entire surface


    def render_circle(self, cx: int, cy: int, radius: int):
        circle = helpers.get_points_in_circle(cx, cy, radius)
        [self.render_image.set_at((pt[0], pt[1]), (255, 255, 255)) for pt in circle]




