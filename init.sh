#!/bin/bash

BASE_DIR=`dirname $0`

# change to the directory this script is running in, so work will
# be relative to a known path
TOP=$(cd $(dirname $0) && pwd)

sudo apt-get install -y --force-yes \
    build-essential python-dev \
    python-pip python-nose python-requests

echo $TOP | sudo tee /usr/local/lib/python2.7/dist-packages/feature_finder.pth

sudo pip install geojson
sudo pip install mock
