import math
import random

from BasicDataStruct import *
from BasicFuncClass import *
from typing import Tuple, List, Dict


class Node:
    def __init__(self, temp_id: str, position: Position, affiliation: Affiliation, node_type: NodeType):
        # 类型校验
        if not isinstance(position, Position):
            raise TypeError("position参数必须是Position类型")
        if not isinstance(affiliation, Affiliation):
            raise TypeError("affiliation参数必须是Affiliation类型")
        if not isinstance(node_type, NodeType):
            raise TypeError("node_type参数必须是NodeType类型")

        self.position: Position = position
        self.affiliation:Affiliation = affiliation
        self.node_type: NodeType = node_type
        self.id: str = temp_id
        self.price: float = 1.0

    def __copy__(self):
        new_node = Node(self.id, self.position.__copy__(), self.affiliation, self.node_type)
        new_node.price = self.price
        return new_node


class MissileNode(Node):
    def __init__(self, temp_id: str, shoot_range_min: float, shoot_range_max: float,
                 precision: float, damage: float, penetration_rate: float,
                 avg_speed: float, price: float):
        super().__init__(temp_id, Position(0.0, 0.0, 0.0), node_type=NodeType.Missile, affiliation=Affiliation.RED)
        self.id = temp_id
        self.vehicle_node: RedStrikeVehicleNode = None
        self.node_type = NodeType.Missile
        self.missile_type = MissileType.DEFAULT
        self.shoot_range_min = shoot_range_min
        self.shoot_range_max = shoot_range_max
        self.precision = precision
        self.damage = damage
        self.penetration_rate = penetration_rate
        self.avg_speed = avg_speed
        self.price = price
        self.K = 0.01

        self.actual_damage_capability: float = 0.0
        # self.cal_actual_damage_capability()

    def __copy__(self):
        new_missile = MissileNode(self.id, self.shoot_range_min, self.shoot_range_max,
                                  self.precision, self.damage,
                                  self.penetration_rate, self.avg_speed, self.price)
        new_missile.K = self.K
        new_missile.missile_type = self.missile_type
        new_missile.actual_damage_capability = self.actual_damage_capability
        return new_missile

    def cal_actual_damage_capability(self):
        self.actual_damage_capability = self.K * self.damage * self.damage / (self.precision * self.precision * self.precision)


class ShortRangedBallisticMissile(MissileNode):
    def __init__(self, id):
        super().__init__(id, 1e4, 3e5, 5.0, 400, 0.5, 700, 30)
        self.missile_type = MissileType.SRBM
        self.K = 0.07
        self.cal_actual_damage_capability()


class MiddleRangedBallisticMissle(MissileNode):
    def __init__(self, id):
        super().__init__(id, 1e5, 1e6, 3.0, 2000, 0.7, 2000, 300)
        self.missile_type = MissileType.MRBM
        self.K = 0.003
        self.cal_actual_damage_capability()


class MiddleRangedCruiseMissile(MissileNode):
    def __init__(self, id):
        super().__init__(id, 5e4, 7e5, 2.0, 1000, 0.6, 600, 200)
        self.missile_type = MissileType.MRCM
        self.K = 0.002
        self.cal_actual_damage_capability()


class RedStrikeVehicleNode(Node):
    def __init__(self, temp_id: str, position: Position, area: Area, ready_time: float, prepare_time: float):
        super().__init__(temp_id, position, Affiliation.RED,NodeType.Vehicle)
        self.missile: MissileNode = None
        self.area = area
        self.current_missile_num = -1
        self.max_missile_num = -1
        self.ready_time = ready_time
        self.prepare_time = prepare_time
        self.actual_ready_time = self.ready_time + self.prepare_time

    def setup_missile(self, missile: MissileNode, missile_num: int):
        self.missile = missile
        self.missile.vehicle_node = self
        self.current_missile_num = missile_num
        self.max_missile_num = missile_num

    def __copy__(self):
        new_vehicle_node = RedStrikeVehicleNode(self.id, self.position.__copy__(), self.area,
                                                self.ready_time, self.prepare_time)
        new_vehicle_node.current_missile_num = self.current_missile_num
        new_vehicle_node.max_missile_num = self.max_missile_num
        new_vehicle_node.missile = self.missile.__copy__()
        new_vehicle_node.missile.vehicle_node = new_vehicle_node
        return new_vehicle_node


class TargetNode(Node):
    def __init__(self, temp_id: str, position: Position, missile_capacity, size: float, price,
                 threat_level, defense_level, expose_duration, expose_time_start):
        super().__init__(temp_id, position, Affiliation.BLUE, NodeType.Target)
        self.size = size
        self.price: int = price
        self.missile_capacity = missile_capacity
        self.threat_level = threat_level
        self.defense_level = defense_level
        self.expose_duration = expose_duration
        self.expose_time_start = expose_time_start
        self.penetration_penalty = 0.0

        if self.threat_level == 1:
            self.penetration_penalty = 0.2
        if self.threat_level == 2:
            self.penetration_penalty = 0.2
        if self.threat_level == 3:
            self.penetration_penalty = 0.05

        self.target_flee_time = expose_duration +expose_time_start
        self.damage_requirement = 1000.0
        self.feasible_fire_action_list: List[FireAction] = []
        self.assigned_fire_action_list: List[FireAction] = []

    def __copy__(self):
        new_node = TargetNode(self.id, self.position.__copy__(), self.missile_capacity, self.size,
                              self.price, self.threat_level, self.defense_level, self.expose_duration,self.expose_time_start)
        new_node.damage_requirement = self.damage_requirement
        return new_node


class XF_launcher(TargetNode):
    def __init__(self, id: str, position:Position, expose_time_start:float):
        super().__init__(id, position, missile_capacity=16, size=3.0, price=80, threat_level=1, defense_level=1,
                         expose_duration=20 * 60, expose_time_start=expose_time_start)
        self.damage_requirement = 400.0


class JBL_launcher(TargetNode):
    def __init__(self, id: str, position:Position, expose_time_start:float):
        super().__init__(id, position, missile_capacity=8, size=6.0, price=110, threat_level=2, defense_level=2,
                         expose_duration=15 * 60, expose_time_start=expose_time_start)
        self.damage_requirement = 200.0


class YC_launcher(TargetNode):
    def __init__(self, id: str, position:Position, expose_time_start:float):
        super().__init__(id, position, missile_capacity=10, size=2.0, price=100, threat_level=3, defense_level=2,
                         expose_duration=10 * 60, expose_time_start=expose_time_start)
        self.damage_requirement = 200.0


class FireAction:
    def __init__(self, target_node: TargetNode, red_launcher_node: RedStrikeVehicleNode, assigned_missile_num,
                 launch_time: float):
        self.target_node: TargetNode = target_node
        self.red_launcher_node: RedStrikeVehicleNode = red_launcher_node
        self.assigned_missile_num = assigned_missile_num
        self.launch_time = launch_time

        self.required_damage_missile_num = 0
        self.cal_required_damage_missile_num()

        self.required_penetration_missile_num = 0
        self.cal_required_penetration_missile_num()

        # 首先移动发射车辆的位置至离目标点最近的发射位置
        temp_coord, temp_distance = BasicGeometryFunc.find_closet_coord_and_distance(self.red_launcher_node.area.generate_area_pos_list(), self.target_node.position)

        self.red_launcher_node.position = temp_coord

        self.node_distance = BasicGeometryFunc.cal_distance_from_to_node(self.target_node.position,
                                                                         self.red_launcher_node.position)
        self.missile_fly_duration = self.node_distance / self.red_launcher_node.missile.avg_speed

    def check_feasibility_step_1(self)->bool:
        if not self.red_launcher_node.missile.shoot_range_min <= self.node_distance <= self.red_launcher_node.missile.shoot_range_max:
            return False

        if self.target_node.size < (self.red_launcher_node.missile.precision - 1e-6):
            return False

        return True

    def assign_missile_num_by_damage_and_penetration(self):
        self.assigned_missile_num = self.required_penetration_missile_num

    def check_is_missile_number_required_meet(self)->bool:
        if self.required_damage_missile_num <= self.red_launcher_node.current_missile_num:
            return True
        else:
            return False

    def cal_launch_time(self)->bool:
        launch_time_min = max(self.red_launcher_node.actual_ready_time, self.target_node.expose_time_start)
        if launch_time_min + self.missile_fly_duration > self.target_node.target_flee_time:
            return False
        launch_time_max = self.target_node.target_flee_time - self.missile_fly_duration
        # TODO: 现在只是随机，需要对齐齐射要求
        self.launch_time = random.uniform(launch_time_min, launch_time_max)
        return True

    def cal_required_damage_missile_num(self):
        self.required_damage_missile_num = math.ceil(self.target_node.damage_requirement / self.red_launcher_node.missile.actual_damage_capability)

    def cal_required_penetration_missile_num(self):
        self.required_penetration_missile_num = math.ceil(self.required_damage_missile_num / (
            self.red_launcher_node.missile.penetration_rate - self.target_node.penetration_penalty))

    def cal_feasibility(self)->bool:
        if self.check_feasibility_step_1():
            return False

        if self.launch_time < self.red_launcher_node.actual_ready_time:
            return False
        if self.launch_time - self.red_launcher_node.prepare_time < self.target_node.expose_time_start:
            return False

        if self.launch_time + self.missile_fly_duration > self.target_node.target_flee_time:
            return False
        if self.assigned_missile_num * self.red_launcher_node.missile.actual_damage_capability < self.target_node.damage_requirement:
            return False

        return True
