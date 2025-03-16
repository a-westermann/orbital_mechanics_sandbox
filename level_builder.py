import json
from classes import *


def load_level(lvl) -> Level:
    with open('levels.json', 'r') as f:
        data = json.load(f)

    bodies = []
    for b in data['bodies']:
        bodies.append(Body(b['x'], b['y'], b['size'], (b['velocity_x'], b['velocity_y']),
                        (b['color_x'], b['color_y'], b['color_z'])))

    goal = Goal((data['goal_x'], data['goal_y']), data['goal_width'], data['goal_height'])
    level = Level(lvl, bodies, goal)
    return level
