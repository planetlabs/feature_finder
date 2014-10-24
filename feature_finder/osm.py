import requests
import json


def run():
    wa_state = [45.1510532655634, -125.41992187499999, 49.15296965617042, -116.630859375]

    airports = get_airport_points(bbox=wa_state)
    print '{} airport points obtained.'.format(len(airports))
    save_to_file(airports, 'airports.json')


def get_airport_points(
        url='http://overpass-api.de/api/interpreter',
        bbox=None):

    airport_node = 'node[\"aeroway\"=\"aerodrome\"]'

    if bbox is None:
        bbox_str=''
    else:
        bbox_str = '({})'.format(', '.join([repr(x) for x in bbox]))

    query_pc = [
        '?data=',
        '[out:json];',
        '{}{};'.format(airport_node, bbox_str),
        'out;'
        ]
    query = ''.join(query_pc)

    r = requests.get(url + query)
    l = json.loads(r.text)
    return l['elements']


def save_to_file(elements_json, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(elements_json))


if __name__ == "__main__":
    run()
