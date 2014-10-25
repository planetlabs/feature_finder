import requests
import geojson
import json


SCENE_URL = "https://api.planet.com/v0/scenes/ortho"
API_KEY_FILE = '../.key'


def query_api(params,
        url = SCENE_URL,
        key_file = API_KEY_FILE):

        # Read API key from file
        with open(key_file, 'r') as f:
            key = f.read()

        # Query API endpoint
        data = requests.get(url, params=params,
            headers={'Authorization': 'api-key ' + key})

        return data


def get_scenes_by_points(points):
    # TODO: change this over to using a single multipoint query
    scenes = []
    for geom in points:
        scenes = scenes + get_intersecting_scenes(geom)
        # scenes.append(get_intersecting_scenes(geom))

    return scenes


def get_intersecting_scenes(geometry_geojson):
        params = {
            "intersects": geojson.dumps(geometry_geojson),
        }

        data = query_api(params)

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

