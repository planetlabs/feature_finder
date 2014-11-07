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
import json
from geojson import Point


def test():
    wa_state = [45.1510532655634, -125.41992187499999, 49.15296965617042, -116.630859375]

    airports = get_airport_points(bbox=wa_state)
    print '{} airport points obtained.'.format(len(airports))

    filename = 'airports.json'
    save_to_file(airports[:5], filename)
    elements = load_elements_from_file(filename)
    print '{} airport points read.'.format(len(elements))


def get_airport_points(
        bbox=None):
    
    airport_query = '\"aeroway\"=\"aerodrome\"'
    r = osm_node_query(airport_query, bbox)
    elements = r['elements']
    points = [Point((x['lon'], x['lat'])) for x in elements]
    return points

def osm_query(
        query, url='http://overpass-api.de/api/interpreter'):
    # Example query (airport points): 'node[\"aeroway\"=\"aerodrome\"]''
    query_pc = [
        '?data=',
        '[out:json];',
        '{};'.format(query),
        'out;'
        ]
    query = ''.join(query_pc)

    r = requests.get(url + query)
    return json.loads(r.text)


def osm_node_query(node_query, bbox):
    if bbox is None:
        bbox_str=''
    else:
        bbox_str = '({})'.format(', '.join([repr(x) for x in bbox]))

    ret = osm_query('node[{}]{}'.format(node_query, bbox_str))
    return ret


def save_to_file(elements_json, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(elements_json))


def load_elements_from_file(filename):
    with open(filename, 'r') as f:
        elements = json.loads(f.read())
    return elements    
    

if __name__ == "__main__":
    test()
