import requests
import json
from geojson import Point


def run():
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
    points = [Point((x['lat'], x['lon'])) for x in elements]
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
    run()
