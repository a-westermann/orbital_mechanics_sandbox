import pygame as pg


class Body:
    def __init__(self, cx: int, cy: int, radius: int, velocity: (float, float), color, static,
                 density: int):
        super().__init__()
        self.comet = False
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.velocity = velocity
        self.soi = radius * 10
        self.mass = radius * 1000000000
        self.default_color = self.color = color
        self.static = static
        self.density = density


class Goal(pg.Rect):
    def __init__(self, pos, width, height):
        super().__init__(pos[0], pos[1], width, height)
        self.color = (0, 255, 0)


class ColorLerpObject:
    def __init__(self, color: (int, int, int), col1: (int, int, int), col2: (int, int, int),
                 step: float = 0.01):
        self.color = color
        self.col1 = col1
        self.col2 = col2
        self.t = 0.0  # Interpolation factor
        self.step = step  # Step size for each frame
        self.forward = True  # Direction of lerp

    def lerp_color(self, c1: (int, int, int), c2: (int, int, int), t: float) -> (int, int, int):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def update_color(self):
        if self.forward:
            self.t += self.step
            if self.t >= 1.0:
                self.t = 1.0
                self.forward = False
        else:
            self.t -= self.step
            if self.t <= 0.0:
                self.t = 0.0
                self.forward = True

        self.color = self.lerp_color(self.col1, self.col2, self.t)




class NoGoZone(pg.Rect, ColorLerpObject):
    def __init__(self, pos, width, height):
        super().__init__(pos[0], pos[1], width, height)
        ColorLerpObject.__init__(self, (255, 0, 0), (255, 0, 0), (125, 0, 0))


class Wormhole:
    def __init__(self, pos, angle):
        self.x = pos[0]
        self.y = pos[1]
        self.length = 100
        self.color = (0, 0, 255)
        self.angle = angle
        import math
        angle_radians = math.radians(self.angle)
        self.end_x = pos[0] + self.length * math.cos(angle_radians)
        self.end_y = pos[1] + self.length * math.sin(angle_radians)
        self.centerx = pos[0] + self.length / 2 * math.cos(angle_radians)
        self.centery = pos[1] + self.length / 2 * math.sin(angle_radians)


class Level:
    def __init__(self, level, name, bodies, goal, nogos, wormholes):
        self.level = level
        self.name = name
        self.bodies = bodies
        self.goal = goal
        self.nogos = nogos
        self.wormholes = wormholes

