from enum import Enum
import random


class Affiliation(Enum):
    RED = "红方"
    BLUE = "蓝方"


class NodeType(Enum):
    Target = "目标节点"
    Vehicle = "打击车辆节点"
    Missile = "导弹节点"


class MissileType(Enum):
    DEFAULT = "default"
    SRBM = "HJD"
    MRBM = "DDD"
    MRCM = "XHD"


class Position:
    def __init__(self, longitude: float, latitude: float, altitude:float):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude

    def __copy__(self):
        new_pos = Position(self.longitude, self.latitude, self.altitude)
        return new_pos


class Area:
    def __init__(self, lon_min: float, lon_max: float, lat_min:float, lat_max: float):
        self.lon_min = lon_min
        self.lon_max = lon_max
        self.lat_min = lat_min
        self.lat_max = lat_max

        self.center_pos:Position = Position((self.lon_min+ self.lon_max) / 2.0, (self.lat_min + self.lat_max) / 2.0, 0.0)

    def generate_position_within_area(self):
        lon_random = random.uniform(self.lon_min, self.lon_max)
        lat_random = random.uniform(self.lat_min, self.lat_max)
        temp_Position = Position(lon_random, lat_random, 0.0)
        return temp_Position

    def generate_area_pos_list(self):

        pos_1 = Position(self.lon_min, self.lat_min, 0.0)
        pos_2 = Position(self.lon_max, self.lat_min, 0.0)
        pos_3 = Position(self.lon_max, self.lat_max, 0.0)
        pos_4 = Position(self.lon_min, self.lat_max, 0.0)

        return [pos_1, pos_2, pos_3, pos_4]
