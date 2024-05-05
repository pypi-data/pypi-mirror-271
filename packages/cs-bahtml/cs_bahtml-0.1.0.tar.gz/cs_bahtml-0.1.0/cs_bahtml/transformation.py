from awpy.data import MAP_DATA
from typing import Tuple



def position_to_csgo(mapname, position):
    """Transforms a position from map to csgo

    Args:
        map_name (string): Map to search
        position (tuple): (X,Y) coordinates

    Returns:
        tuple
    """
    start_x = MAP_DATA[mapname]["x"]
    start_y = MAP_DATA[mapname]["y"]
    scale = MAP_DATA[mapname]["scale"]
    x = position[0]*scale + start_x
    y = -(position[1] * scale -start_y)
    return (x, y)

def find_closest_area(map_name, point, flat=False):
    """Finds the closest area in the nav mesh. Searches through all the areas by comparing point to area centerpoint.

    Args:
        map_name (string): Map to search
        point (list): Point as a list [x,y,z]

    Returns:
        A dict containing info on the closest area
    """
    if map_name not in NAV.keys():
        raise ValueError("Map not found.")
    if len(point) != 3:
        raise ValueError("Point must be a list [X,Y,Z]")
    closest_area = {"mapName": map_name, "areaId": None, "distance": 999999}
    for area in NAV[map_name].keys():
        avg_x = (
            NAV[map_name][area]["northWestX"] + NAV[map_name][area]["southEastX"]
        ) / 2
        avg_y = (
            NAV[map_name][area]["northWestY"] + NAV[map_name][area]["southEastY"]
        ) / 2
        avg_z = (
            NAV[map_name][area]["northWestZ"] + NAV[map_name][area]["southEastZ"]
        ) / 2
        if flat:
            dist = np.sqrt(
                (point[0] - avg_x) ** 2 + (point[1] - avg_y) ** 2
            )
        else:
            dist = np.sqrt(
                (point[0] - avg_x) ** 2 + (point[1] - avg_y) ** 2 + (point[2] - avg_z) ** 2
            )
        if dist < closest_area["distance"]:
            closest_area["areaId"] = area
            closest_area["distance"] = dist
    return closest_area