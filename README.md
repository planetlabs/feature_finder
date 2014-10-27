feature_finder
==============

Finds scenes that overlap OSM features by feature category (e.g. airports) using the OSM overpass api and Planet scenes api.

The Planet scenes api key should be stored as text in .key in the root directory. This file is ignored by git.

TODO: transition api key to command-line argument

# Dependencies

* geojson
* requests
* nosetests

# Dev setup

## Vagrant

    # This should get you up and running with a new development environment
    vagrant up
    vagrant ssh

    # Your files live in /vagrant :O
    cd /vagrant

## Tests

To run the tests:

	nosetests
