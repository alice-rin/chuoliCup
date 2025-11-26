from BasicDataStruct import *
import math


class BasicGeometryFunc:
    @staticmethod
    def cal_distance_from_to_node(pos_1: Position, pos_2: Position):
        lat1_rad = math.radians(pos_1.latitude)
        lon1_rad = math.radians(pos_1.longitude)
        lat2_rad = math.radians(pos_2.latitude)
        lon2_rad = math.radians(pos_2.longitude)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 -a))

        R = 6371.0 * 1e3
        return R * c
