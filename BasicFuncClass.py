from BasicDataStruct import *
import math
from typing import List, Dict

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

    @staticmethod
    def project_point_to_line(point:Position, line_start:Position, line_end:Position):
        """将点投影到线段上，返回投影点坐标"""
        x, y, z = point.longitude, point.latitude, point.altitude
        x1, y1, z1 = line_start.longitude, line_start.latitude, line_start.altitude
        x2, y2, z2 = line_end.longitude, line_end.latitude, line_end.altitude

        # 计算线段向量
        dx, dy, dz = x2 - x1, y2 - y1, z2- z1

        # 如果线段是一个点
        if dx == 0 and dy == 0:
            return line_start

        # 计算投影参数t
        t = ((x - x1) * dx + (y - y1) * dy) / (dx ** 2 + dy ** 2)

        # 限制t在[0,1]范围内，确保投影点在线段上
        t = max(0, min(1, t))

        # 计算投影点坐标
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        proj_z = z1 + t * dz

        return Position(proj_x, proj_y, proj_z)
    @staticmethod
    def find_closet_coord_and_distance(area_pos_list:List[Position], target_pos:Position):

        closet_point:Position = Position(0.0, 0.0,0.0)
        min_distance = 1e10

        for i in range(len(area_pos_list)-1):
            point_start = area_pos_list[i]
            point_end = area_pos_list[i+1]

            temp_project_coord = BasicGeometryFunc.project_point_to_line(target_pos, point_start, point_end)

            distance =BasicGeometryFunc.cal_distance_from_to_node(temp_project_coord, target_pos)

            if min_distance > distance:
                min_distance = distance
                closet_point = temp_project_coord
        return closet_point, min_distance


