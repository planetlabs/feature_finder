import requests
import geojson
import json


def run():
    test()

def test():
    dallas_tx = {"coordinates": [-96.7967,32.7695], "type": "Point"}
    cedar_rapids_ia_airport = {"coordinates": [-91.7046, 41.8854], "type": "Point"}
    points = [dallas_tx, cedar_rapids_ia_airport]

    params = {
        "intersects": geojson.dumps(points[0]),
    } 
    data = planet_query(params)
    scenes_0 = data.json()["features"]

    scenes_1 = get_intersecting_scenes(points[0])
    print '{} ?= {}'.format(len(scenes_0), len(scenes_1))

    scenes_2 = get_intersecting_scenes(points[1])

    scenes_tot = get_scenes_by_points(points)
    print '{} + {} ?= {}'.format(len(scenes_1), len(scenes_2), len(scenes_tot))



def get_key(key_file='../.key'):
    with open('../.key', 'r') as f:
        key = f.read()
    return key


def get_scenes_by_points(points):
    # TODO: change this over to using a single multipoint query
    scenes = []
    for geom in points:
        scenes = scenes + get_intersecting_scenes(geom)
        # scenes.append(get_intersecting_scenes(geom))

    return scenes

def planet_query(params,
        url = "https://api.planet.com/v0/scenes/ortho"):
        key = get_key()

        data = requests.get(url, params=params,
            headers={'Authorization': 'api-key ' + key})

        return data

def get_intersecting_scenes(geometry_geojson):
        params = {
            "intersects": geojson.dumps(geometry_geojson),
        }

        data = planet_query(params)

        scenes = data.json()["features"]

        return scenes

def get_thumbnails(scenes):
    return [scene['properties']['links']['thumbnail'] for scene in scenes]

def get_scenes_acquired(scenes):
    return [scene['properties']['acquired'] for scene in scenes]

def get_scenes_footprint(scenes):
    return [scene['geometry'] for scene in scenes]

def save(json_dict, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_dict))    

if __name__ == '__main__':
    run()
