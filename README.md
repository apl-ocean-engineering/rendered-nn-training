# rendered-nn-training

This project aims to generate a synthetic training set of artificially rendered images to feed to a neural network that can then be used to identify real-world camera images. It uses the Panda3D package for Python to render a 3D model of the target object in a variety of positions and orientations in a realistic environment.

Written and tested with Panda release 1.10.x and Python 2.7 (but should work in 3.x as well).

## Usage
Run **python multimine.py -h** for usage/parameter guidelines. Directory addresses need to be manually updated when used on other machines.

Currently multimine.py is the only necessary script; it stands alone once necessary directory pointers have been updated.

## Dependencies
Panda3D: **sudo pip install --pre --extra-index-url https://archive.panda3d.org/branches/release/1.10.x panda3d** OR buildbot direct link: https://buildbot.panda3d.org/downloads/2c9d16f62e2a60ae1437d2b725beefcb27c3f55a/

Python: https://www.python.org/downloads/
