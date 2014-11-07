'''
Copyright 2014, Planet Labs, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

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



