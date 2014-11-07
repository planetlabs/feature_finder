feature_finder
==============

Feature Finder is a Python library for finding [Planet Labs](https://www.planet.com/) scenes that overlap (OpenStreeMap)[http://www.openstreetmap.org/] feature categories. While support is limited to airports at this time, support will be added for additional feature categories over time.

OSM features are obtained by using the [OSM overpass API](http://wiki.openstreetmap.org/wiki/API_v0.6) and Planet Labs scenes are obtained using [Planet Lab's Scenes REST API](https://www.planet.com/docs/v0/scenes/?python).

The Planet Labs scenes api key should be stored as text in the file '.key,' stored in the root directory. This file is ignored by git.

# Dependencies

This library uses Python 2.7 and depends on the following Python libraries:
* geojson
* requests
* nose

# Development Setup

## Vagrant

To support a repeatable and standard development environment, this library includes a [Vagrant](https://www.vagrantup.com/) virtual machine. This virtual machine installs all of the repository depencencies on startup. 

To use this virtual machine, first ensure a virtualization provider, such as [VirtualBox](https://www.virtualbox.org/) is installed. Next, follow these steps:

    # Run this in the repository root directory, where 'Vagrantfile' resides
    vagrant up
    vagrant ssh

    # The VM shares the repository directory with the host computer
    # Within the VM, the repository files are in /vagrant
    cd /vagrant

## Tests

To run the tests:

	nosetests
