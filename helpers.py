

def get_points_in_circle(cx: int, cy: int, radius: int) -> []:
    pts = []
    r2 = radius**2
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                pts.append((x, y))
    return pts

