import json

import osm, planet

def run():
    wa_state = [45.1510532655634, -125.41992187499999, 49.15296965617042, -116.630859375]
    airports_file = 'WA_airports.json'
    scenes_file = 'WA_airport_scenes.json'

    rerun_osm = True
    rerun_scenes = True
    if not rerun_osm:
        try:
            airports = load(airports_file)
        except:
            airports = get_airports(bbox=wa_state)
    else:
        airports = get_airports(bbox=wa_state)

    if not rerun_scenes:
        try:
            scenes = load(scenes_file)
        except:
            scenes = get_scenes(airports)
    else:
        scenes = get_scenes(airports)

    for scene in scenes:
        print planet.get_thumbnail(scene, large=True)

    print "{} scenes overlap the {} airports. ".format(len(scenes), len(airports))

def get_airports(bbox, out_filename=None):
    airports = osm.get_airport_points(bbox=bbox)
    if out_filename is not None:
        save(airports, out_filename)
    return airports

def get_scenes(points, out_filename=None):
    scenes = planet.get_scenes_by_points(points)
    if out_filename is not None:
        save(scenes, out_filename)

    return scenes

def load(filename):
    with open(filename, 'r') as f:
        elements = json.loads(f.read())
    return elements  

def save(json_dict, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_dict))

if __name__ == '__main__':
    run()
