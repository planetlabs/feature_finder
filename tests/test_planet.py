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
        scenes_0 = data.json()["features"]

        self.assertTrue(len(scenes_0) >= 2)

    def test_get_intersecting_scenes(self):

        scenes_1 = planet.get_intersecting_scenes(self.test_points[0])
        self.assertTrue(len(scenes_1) >= 2)

    def test_get_scenes_by_points(self):

        scenes_1 = planet.get_intersecting_scenes(self.test_points[0])
        scenes_2 = planet.get_intersecting_scenes(self.test_points[1])

        scenes_tot = planet.get_scenes_by_points(self.test_points)
        self.assertEqual(len(scenes_tot), len(scenes_1) + len(scenes_2))

if __name__ == '__main__':
    unittest.main()
