"""Top-level package for cs_bahtML."""

__author__ = """Anton Baht"""
__email__ = 'anton@baht.dk'
__version__ = '0.1.0'


import os
import json
from PIL import Image

PATH = os.path.join(os.path.dirname(__file__), "")

RADARS = {}

for radar in os.listdir(PATH):
    if radar.endswith(".png"):
        RADARS[radar[:-10]] = Image.open(PATH+radar)

with open(PATH + "map_data.json", encoding="utf8") as map_data:
    MAP_DATA = json.load(map_data)

if __name__ == "__main__":
    RADARS["de_inferno"].show()
    print(MAP_DATA["de_nuke"])