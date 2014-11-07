#!/usr/bin/env python

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
import argparse
import json
import sys

import osm, planet

def get_arg_parser():
    aparser = argparse.ArgumentParser(
        description='Find scenes overlapping features of a certain type.')

    aparser.add_argument('--skip-features', action='store_true')
    aparser.add_argument('-ff', '--feature-file', 
        help=('Features are written to this. If \'--skip-features\' flag is used, ' +
            'features are read from this file.'),
        default='features.json')    
    aparser.add_argument('--skip-scenes', action='store_true')
    aparser.add_argument('-sf', '--scene-file',
        help='Scenes are written to this file.',
        default='scenes.json')
    return aparser


def run(rawargs):
    args = get_arg_parser().parse_args(rawargs[1:])

    wa_state = [45.1510532655634, -125.41992187499999, 49.15296965617042, -116.630859375]

    bbox = wa_state
    if args.skip_features:
        features = load(args.feature_file)
    else:
        features = osm.get_feature_points('airports', bbox=bbox)  
        save(features, args.feature_file)

    print "{} features. Trimming to first 100 due to Planet Scenes API limit".format(len(features))
    features = features[:100]
    
    if not args.skip_scenes:
        scenes = planet.get_scenes_by_points(features)
        save(scenes, args.scene_file)

        for scene in scenes:
            print planet.get_thumbnail(scene, large=True)

        print "{} overlapping scenes. ".format(len(scenes))


def load(filename):
    with open(filename, 'r') as f:
        elements = json.loads(f.read())
    return elements  


def save(json_dict, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_dict))


if __name__ == '__main__':
    run(sys.argv)
