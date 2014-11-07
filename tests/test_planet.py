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

import unittest

import mock
import geojson
from feature_finder import planet

#TODO: Mock all requests calls
class Tests(unittest.TestCase):
    def test_query_api(self):
        # Dallas, TX
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
        # Dallas, TX
        test_point = {"coordinates": [-96.7967, 32.7695], "type": "Point"}
        scenes = planet.get_intersecting_scenes(test_point)
        self.assertTrue(len(scenes) >= 2)

    def test_get_scenes_by_points(self):
        # Dallas, TX, Cedar Rapids Airport
        test_points = [{"coordinates": [-96.7967, 32.7695], "type": "Point"},
                       {"coordinates": [-91.7046, 41.8854], "type": "Point"}]
        # test_points = [{"type": "Point", "coordinates": [-123.3904221, 48.4253301]}, {"type": "Point", "coordinates": [-123.0071356, 49.0745313]}]
        scenes_1 = planet.get_intersecting_scenes(test_points[0])
        scenes_2 = planet.get_intersecting_scenes(test_points[1])
        scenes_test = planet.get_scenes_by_points(test_points)

        # For some reason len(scenes_test) is 5 while len(scenes_1) is 2 and
        # len(scenes_2) is 1 (5!=3)
        self.assertTrue(len(scenes_test) >=len(scenes_1) + len(scenes_2))

    def test_get_thumbnail(self):
        # Dallas, TX, Cedar Rapids Airport
        test_point = {"coordinates": [-96.7967, 32.7695], "type": "Point"}
        scenes = planet.get_intersecting_scenes(test_point)

        thumb = planet.get_thumbnail(scenes[0])

if __name__ == '__main__':
    unittest.main()
