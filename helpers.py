from classes import Body
import math
import pygame as pg


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


def point_near_line(point, start, end, max_distance=5):
    px, py = point
    x1, y1 = start
    x2, y2 = end

    # Vector AB (line segment) and AP (point to start of line)
    line_vec = pg.Vector2(x2 - x1, y2 - y1)
    point_vec = pg.Vector2(px - x1, py - y1)

    # Project point_vec onto line_vec to find closest point on infinite line
    line_length_sq = line_vec.length_squared()
    if line_length_sq == 0:
        return False  # Avoid division by zero (degenerate case: line is a point)

    projection_factor = max(0, min(1, point_vec.dot(line_vec) / line_length_sq))
    closest_x = x1 + projection_factor * line_vec.x
    closest_y = y1 + projection_factor * line_vec.y

    # Check if point is within max_distance of closest point
    distance = math.hypot(px - closest_x, py - closest_y)
    return distance <= max_distance


def rotate_vector(vector, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    rotated_x = vector.x * math.cos(angle_radians) - vector.y * math.sin(angle_radians)
    rotated_y = vector.x * math.sin(angle_radians) + vector.y * math.cos(angle_radians)
    return pg.Vector2(rotated_x, rotated_y)
