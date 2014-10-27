import requests
import geojson


SCENE_URL = "https://api.planet.com/v0/scenes/ortho"
API_KEY_FILE = '../.key'


def query_api(params, key=None, url=SCENE_URL):
    if key is None:
        key = read_key_file()

    data = requests.get(url, params=params,
        headers={'Authorization': 'api-key ' + key})

    return data


def read_key_file(key_file=API_KEY_FILE):
    # Read API key from file
    with open(key_file, 'r') as f:
        key = f.read() 
    return key   


def get_scenes_by_points(points):
    mp = geojson.MultiPoint([point['coordinates'] \
        for point in points])
    scenes = get_intersecting_scenes(mp)

    return scenes


def get_intersecting_scenes(geometry_geojson):
    params = {
        "intersects": geojson.dumps(geometry_geojson),
    }

    data = query_api(params)
    scenes = data.json()["features"]
    return scenes


def get_thumbnail(scene, large=False):
    thumb = scene['properties']['links']['thumbnail']
    if large:
        thumb = '{}?size=lg'.format(thumb)
    return thumb



