from enum import Enum
import random
import math

class Affiliation(Enum):
    RED = "红方"
    BLUE = "蓝方"


class NodeType(Enum):
    Target = "目标节点"
    Vehicle = "打击车辆节点"
    Missile = "导弹节点"


class MissileType(Enum):
    DEFAULT = "default"
    SRBM = "火箭弹"
    MRBM = "弹道弹"
    MRCM = "巡航弹"


class Position:
    def __init__(self, longitude: float, latitude: float, altitude:float):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude

    def __copy__(self):
        new_pos = Position(self.longitude, self.latitude, self.altitude)
        return new_pos

    def __eq__(self, other):

        if self.latitude == other.latitude and self.longitude == other.longitude and self.altitude == other.altitude:
            return True
        return False

    def __sub__(self, other):
        lat1_rad = math.radians(self.latitude)
        lon1_rad = math.radians(self.longitude)
        lat2_rad = math.radians(other.latitude)
        lon2_rad = math.radians(other.longitude)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        R = 6371.0 * 1e3
        return R * c

class Area:
    def __init__(self, lon_min: float, lon_max: float, lat_min:float, lat_max: float):
        self.name = ""
        self.lon_min = lon_min
        self.lon_max = lon_max
        self.lat_min = lat_min
        self.lat_max = lat_max

        self.center_pos:Position = Position((self.lon_min+ self.lon_max) / 2.0, (self.lat_min + self.lat_max) / 2.0, 0.0)

    def set_name(self, name: str):
        self.name = name

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
