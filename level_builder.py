import json
from classes import *


def load_level(lvl) -> Level:
    with open('levels.json', 'r') as f:
        data = json.load(f)

    lvl_data = data['levels'][lvl]
    lvl_name = lvl_data['name']
    bodies = []
    for i, b in enumerate(lvl_data['bodies']):
        density = b['density'] if 'density' in b else 1
        bodies.append(Body(b['x'], b['y'], b['size'], (b['velocity_x'], b['velocity_y']),
                           (b['color_x'], b['color_y'], b['color_z']), b['static'], density))
        if i == 0:
            bodies[-1].comet = True

    goal = Goal((lvl_data['goal_x'], lvl_data['goal_y']), lvl_data['goal_width'], lvl_data['goal_height'])

    nogos = []
    if 'nogos' in lvl_data:
        for i, n in enumerate(lvl_data['nogos']):
            nogos.append(NoGoZone((n['x'], n['y']), n['width'], n['height']))

    wormholes = []
    if 'wormholes' in lvl_data:
        for i, w in enumerate(lvl_data['wormholes']):
            wormholes.append(Wormhole((w['x'], w['y']), w['angle']))


    level = Level(lvl, lvl_name, bodies, goal, nogos, wormholes)
    return level
