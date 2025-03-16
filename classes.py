import pygame as pg


class Body:
    def __init__(self, cx: int, cy: int, radius: int, velocity: (float, float), color):
        super().__init__()
        self.comet = False
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.velocity = velocity
        self.soi = radius * 10
        self.mass = radius * 1000000000
        self.default_color = self.color = color


class Goal(pg.Rect):
    def __init__(self, pos, width, height):
        super().__init__(pos[0], pos[1], width, height)
        self.color = (255, 255, 255)


class Level:
    def __init__(self, level, bodies, goal):
        self.level = level
        self.bodies = bodies
        self.goal = goal
