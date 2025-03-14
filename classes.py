class Body:
    def __init__(self, cx: int, cy: int, radius: int, velocity: (float, float), color):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.velocity = velocity
        self.soi = radius * 10
        self.default_color = self.color = color
