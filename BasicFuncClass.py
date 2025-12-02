from BasicDataStruct import *
import math
from typing import List

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

    # 这个是给定经纬度、朝向和距离，来计算新的经纬度
    @staticmethod
    def calculate_destination_haversine(pos_A:Position, bearing, distance):
        """
        使用Haversine公式根据起点、方位角和距离计算终点坐标

        参数:
        lat: 起点纬度（度）
        lon: 起点经度（度）
        bearing: 方位角（度，0°=正北，90°=正东，180°=正南，270°=正西）
        distance: 距离（米）

        返回:
        (lat2, lon2): 终点经纬度（度）
        """
        R = 6371000  # 地球平均半径（米）

        # 将角度转换为弧度
        lat_rad = math.radians(pos_A.latitude)
        lon_rad = math.radians(pos_A.longitude)
        bearing_rad = math.radians(bearing)

        # 计算角距离
        angular_distance = distance / R

        # 计算新纬度
        lat2_rad = math.asin(math.sin(lat_rad) * math.cos(angular_distance) +
                             math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing_rad))

        # 计算新经度
        lon2_rad = lon_rad + math.atan2(math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat_rad),
                                        math.cos(angular_distance) - math.sin(lat_rad) * math.sin(lat2_rad))

        # 将弧度转换回角度
        lat2 = math.degrees(lat2_rad)
        lon2 = math.degrees(lon2_rad)

        return Position(lon2, lat2, pos_A.altitude)

    @staticmethod
    def calculate_bearing_from_A_to_B(pos_A:Position, pos_B:Position):
        """
        计算从点A到点B的连线相对于点B的朝向（方位角）

        参数:
        latA, lonA: 点A的纬度和经度（十进制度数）
        latB, lonB: 点B的纬度和经度（十进制度数）

        返回:
        bearing: 相对于点B的朝向角度（度），0°表示正北，顺时针增加
        """
        # 将经纬度转换为弧度[1,2](@ref)
        latA_rad = math.radians(pos_A.latitude)
        lonA_rad = math.radians(pos_A.longitude)
        latB_rad = math.radians(pos_B.latitude)
        lonB_rad = math.radians(pos_B.longitude)

        # 计算经度差[1,6](@ref)
        dLon = lonA_rad - lonB_rad  # 注意这里是A-B，因为我们想要从B看A的方向

        # 计算方位角[1,6](@ref)
        y = math.sin(dLon) * math.cos(latA_rad)
        x = math.cos(latB_rad) * math.sin(latA_rad) - math.sin(latB_rad) * math.cos(latA_rad) * math.cos(dLon)

        # 计算初始方位角（弧度）[1](@ref)
        initial_bearing = math.atan2(y, x)

        # 将弧度转换为度，并归一化到0-360度范围[1,6](@ref)
        initial_bearing_deg = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing_deg + 360) % 360

        return compass_bearing

    @staticmethod
    def point_in_polygon_ray_casting(pos_A:Position, polygon_coords:List[Position]):
        """
        使用射线法判断点是否在多边形内
        :param point_lon: 点的经度
        :param point_lat: 点的纬度
        :param polygon_coords: 多边形顶点坐标列表
        :return: Boolean, 点是否在多边形内
        """
        x, y = pos_A.longitude, pos_A.latitude
        n = len(polygon_coords)
        inside = False

        # 确保多边形闭合
        if polygon_coords[0] != polygon_coords[-1]:
            polygon_coords.append(polygon_coords[0])

        p1_lon, p1_lat = polygon_coords[0].longitude, polygon_coords[0].latitude
        for i in range(1, n + 1):
            p2_lon, p2_lat = polygon_coords[i % n].longitude, polygon_coords[i % n].latitude

            # 检查点是否在多边形的边上
            if (min(p1_lon, p2_lon) <= x <= max(p1_lon, p2_lon) and
                    min(p1_lat, p2_lat) <= y <= max(p1_lat, p2_lat)):
                # 点在边界上
                return True

            # 射线与边相交判断
            if (p1_lat > y) != (p2_lat > y):  # 点在两个端点的垂直范围内
                if p1_lat == p2_lat:  # 水平边
                    x_intersect = (p1_lon + p2_lon) / 2
                else:
                    x_intersect = (y - p1_lat) * (p2_lon - p1_lon) / (p2_lat - p1_lat) + p1_lon

                if x <= x_intersect:
                    inside = not inside

            p1_lon, p1_lat = p2_lon, p2_lat

        return inside