import unittest
import geojson
from feature_finder import planet


class Test(unittest.TestCase):
    def setup(self):
        self.dallas_tx = {"coordinates": [-96.7967,32.7695], "type": "Point"}
        self.cedar_rapids_ia_airport = {"coordinates": [-91.7046, 41.8854], "type": "Point"}
        self.test_points = [self.dallas_tx, self.cedar_rapids_ai_airport]

    def test_planet_query(self):
        test_point = self.dallas_tx
        params = {
            "intersects": geojson.dumps(test_point),
        } 
        data = planet.query_api(params)
        scenes = data.json()["features"]

        self.assertTrue(len(scenes) >= 2)

    def test_get_intersecting_scenes(self):
        scenes = planet.get_intersecting_scenes(self.test_points[0])
        self.assertTrue(len(scenes) >= 2)

    def test_get_scenes_by_points(self):
        scenes_1 = planet.get_intersecting_scenes(self.test_points[0])
        scenes_2 = planet.get_intersecting_scenes(self.test_points[1])
        scenes_test = planet.get_scenes_by_points(self.test_points)
        self.assertEqual(len(scenes_test), len(scenes_1) + len(scenes_2))

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
