import requests
import geojson


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
    mp = geojson.MultiPoint([geojson.utils.coords(point) \
        for point in points])
    scenes = get_intersecting_scenes(mp)

    return scenes


def get_intersecting_scenes(geometry_geojson):
    params = {
        "intersects": geojson.dumps(geometry_geojson),
    }

    data = query_api(params)

    elements = data.json()["features"]
    scenes = [create_scene(elem) for elem in elements]

    return scenes


def create_scene(o):
    """Create an instance of Scene from a dict, o. If o does not
    match a Python feature object, simply return o. This function serves as a
    json decoder hook."""
    try:
        geom = o['geometry']
        p = o['properties']
        return Scene(footprint=geom, acquired=p['acquired'],
            thumbnail=p['links']['thumbnail'])
    except (KeyError, TypeError):
        pass
    return o


class Scene(object):
    def __init__(self, footprint=None, acquired=None,
            thumbnail=None):
        """Initialize."""
        self.footprint = footprint
        self.acquired = acquired
        self.thumbnail = thumbnail
        self.thumbnail_lrg = '{}?size=lg'.format(thumbnail)


