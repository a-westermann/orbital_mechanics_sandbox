from classes import Body


def get_points_in_circle(cx: int, cy: int, radius: int) -> []:
    # Very slow when dealing with a large circle
    pts = []
    r2 = radius**2
    cx, cy = int(cx), int(cy)
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                pts.append((x, y))
    return pts


def get_dist(cx1: int, cx2: int, cy1: int, cy2: int) -> int:
    return int(abs(cx1 - cx2) + abs(cy1 - cy2))


def get_grav_accel(b1: Body, b2: Body, dist: int):
    G = 6.6743 * 10 ** -11
    return G * b2.mass / (dist ** 2)
