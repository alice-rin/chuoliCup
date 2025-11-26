import random

from Node import *
from BasicDataStruct import *


class ScenarioGenerator:
    def __init__(self):
        self.blue_side_list = []
        self.red_side_list = []

    def createScenario(self):
        # Blue
        area_1 = Area(121.07, 121.65, 24.34, 24.98)
        area_2 = Area(120.61, 120.97, 24.34, 24.98)
        area_3 = Area(121.19, 121.43, 23.34, 23.91)
        area_4 = Area(120.53, 121.08, 23.14, 23.61)
        area_5 = Area(121.05, 121.23, 22.91, 23.07)
        area_6 = Area(120.75, 120.89, 22.08, 22.87)
        area_list = [area_1, area_2, area_3, area_4, area_5, area_6]

        xf_base_id_index = 100
        jbl_base_id_index = 200
        yc_base_id_index = 300
        for i in range(6):
            temp_id = xf_base_id_index + i + 1
            temp_area: Area = random.choice(area_list)
            temp_position:Position = temp_area.generate_position_within_area()
            temp_launcher = XF_launcher(str(temp_id), temp_position, 0)
            self.blue_side_list.append(temp_launcher)

        for i in range(8):
            temp_id = jbl_base_id_index + i + 1
            temp_area: Area = random.choice(area_list)
            temp_position:Position = temp_area.generate_position_within_area()
            random_expose_time = random.uniform(0, 5 * 60)
            temp_launcher = JBL_launcher(str(temp_id), temp_position, random_expose_time)
            self.blue_side_list.append(temp_launcher)

        for i in range(10):
            temp_id = yc_base_id_index + i + 1
            temp_area: Area = random.choice(area_list)
            temp_position:Position = temp_area.generate_position_within_area()
            random_expose_time = random.uniform(0, 5 * 60)
            temp_launcher = YC_launcher(str(temp_id), temp_position, random_expose_time)
            self.blue_side_list.append(temp_launcher)

        # Red
        area_ballistic_1 = Area(118.82, 120.47, 29.50, 30.62)
        area_ballistic_2 = Area(116.01, 117.35, 28.19, 29.58)
        area_ballistic_3 = Area(113.74, 115.21, 26.43, 27.96)
        area_ballistic_4 = Area(111.96, 114.18, 22.53, 25.44)
        area_ballistic_list = [area_ballistic_1, area_ballistic_2, area_ballistic_3, area_ballistic_4]

        area_cruise_1 = Area(118.85, 121.22, 27.84, 28.95)
        area_cruise_2 = Area(116.46, 119.37, 26.47, 27.46)
        area_cruise_3 = Area(115.16, 117.85, 24.84, 26.12)
        area_cruise_4 = Area(114.80, 116.61, 23.39, 24.40)
        area_cruise_list = [area_cruise_1, area_cruise_2, area_cruise_3, area_cruise_4]

        area_SRBM_1 = Area(118.95, 119.41, 25.57, 25.88)
        area_SRBM_2 = Area(118.26, 118.83, 24.98, 25.32)
        area_SRBM_3 = Area(117.95, 118.57, 24.66, 24.88)
        area_SRBM_list = [area_SRBM_1, area_SRBM_2, area_SRBM_3]

        ballistic_base_id_index = 1000
        cruise_base_id_index = 1100
        SRBM_base_id_index = 1200

        for i in range(4):
            temp_id = ballistic_base_id_index + i + 1
            temp_area: Area = area_ballistic_list[i]
            temp_position:Position = temp_area.generate_position_within_area()
            temp_ready_time = random.uniform(0, 4 * 60)
            temp_red_launcher = RedStrikeVehicleNode(str(temp_id), temp_position, temp_area, temp_ready_time, 40)
            temp_missile = MiddleRangedBallisticMissle(str(temp_id))
            temp_red_launcher.setup_missile(temp_missile, 15)
            self.red_side_list.append(temp_red_launcher)

        for i in range(4):
            temp_id = cruise_base_id_index + i + 1
            temp_area: Area = area_cruise_list[i]
            temp_position:Position = temp_area.generate_position_within_area()
            temp_ready_time = random.uniform(0, 4 * 60)
            temp_red_launcher = RedStrikeVehicleNode(str(temp_id), temp_position, temp_area, temp_ready_time, 20)
            temp_missile = MiddleRangedCruiseMissile(str(temp_id))
            temp_red_launcher.setup_missile(temp_missile, 25)
            self.red_side_list.append(temp_red_launcher)

        for i in range(3):
            temp_id = SRBM_base_id_index + i + 1
            temp_area: Area = area_SRBM_list[i]
            temp_position:Position = temp_area.generate_position_within_area()
            temp_ready_time = random.uniform(0, 4 * 60)
            temp_red_launcher = RedStrikeVehicleNode(str(temp_id), temp_position, temp_area, temp_ready_time, 10)
            temp_missile = ShortRangedBallisticMissile(str(temp_id))
            temp_red_launcher.setup_missile(temp_missile, 100)
            self.red_side_list.append(temp_red_launcher)
