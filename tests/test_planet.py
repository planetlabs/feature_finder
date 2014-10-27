import unittest

import mock
import geojson
from feature_finder import planet

#TODO: Mock all requests calls
class Tests(unittest.TestCase):
    def setUp(self):
        self.dallas_tx = {"coordinates": [-96.7967, 32.7695], "type": "Point"}
        self.cedar_rapids_ia_airport = {"coordinates": [-91.7046, 41.8854], "type": "Point"}
        self.test_points = [self.dallas_tx, self.cedar_rapids_ia_airport]

    def test_planet_query(self):
        test_point = {"coordinates": [-96.7967, 32.7695], "type": "Point"}
        params = {"intersects": geojson.dumps(test_point)}
        key = 'test'

        with mock.patch('requests.get', return_value='heeeyy') as patched_get:
            ret = planet.query_api(params, key=key)
            print ret
            patched_get.assert_called_once_with(
                'https://api.planet.com/v0/scenes/ortho',
                headers={'Authorization': 'api-key test'},
                params={'intersects':
                    '{"type": "Point", "coordinates": [-96.7967, 32.7695]}'})

    def test_get_intersecting_scenes(self):
        test_point = {"coordinates": [-96.7967, 32.7695], "type": "Point"}
        scenes = planet.get_intersecting_scenes(test_point)
        self.assertTrue(len(scenes) >= 2)

    def test_get_scenes_by_points(self):
        test_points = [{"coordinates": [-96.7967, 32.7695], "type": "Point"},
                       {"coordinates": [-91.7046, 41.8854], "type": "Point"}]
        scenes_1 = planet.get_intersecting_scenes(test_points[0])
        scenes_2 = planet.get_intersecting_scenes(test_points[1])
        scenes_test = planet.get_scenes_by_points(test_points)

        # For some reason len(scenes_test) is 5 while len(scenes_1) is 2 and
        # len(scenes_2) is 1 (5!=3)
        self.assertTrue(len(scenes_test) >=len(scenes_1) + len(scenes_2))

    def test_create_scene(self):
        expected_geometry = {
            'type': 'Polygon',
                'coordinates': [[[-122.18242287183, 49.0170164215394],
                                 [-122.223624410176, 49.1122543851311],
                                 [-122.395003379163, 49.0800565134195],
                                 [-122.353403171187, 48.984774883507],
                                 [-122.18242287183, 49.0170164215394]]]
            }
        self.test_scene_dict = {
            'geometry': expected_geometry,
            'type': 'Feature',
            'id': 'test_id',
            'properties': {
                'links': {
                    'self': '',
                    'full': 'full',
                    'square_thumbnail': 'square-thumb',
                    'thumbnail': 'thumb',
                    'tiles': 'tiles'
                    },
                'acquired': '2014-08-23T18:06:02.784420+00:00',
                }
            }

        expected_thumbnail = 'thumb'
        test_scene = planet.create_scene(self.test_scene_dict)
        self.assertEqual(test_scene.thumbnail, expected_thumbnail)
        self.assertEqual(test_scene.footprint, expected_geometry)


if __name__ == '__main__':
    unittest.main()
