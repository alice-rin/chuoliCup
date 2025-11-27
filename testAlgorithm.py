from Chromosome import *
from ScenarioGenerator import *
import time



if __name__ == "__main__":

    # 测试功能===============================
    # cruise_area = Area(0, 1, 0, 1)
    # target_area = Area(121.07, 121.65, 24.34, 24.98)
    # target_pos = Position(2.0, 0.5, 0.0)
    # temp_coord, temp_distance = BasicGeometryFunc.find_closet_coord_and_distance(cruise_area.generate_area_pos_list(), target_pos)
    # temp_distance_1 = BasicGeometryFunc.cal_distance_from_to_node(target_pos, cruise_area.center_pos)
    # 测试通过==================================

    start_time = time.time()

    temp_scenario_generator = ScenarioGenerator()
    temp_scenario_generator.createScenario()

    temp_chromosome = Chromosome(temp_scenario_generator.red_side_list, temp_scenario_generator.blue_side_list)
    temp_chromosome.generate_chromosome_random()#
    temp_chromosome.print_chromosome()

    temp_evaluator = ChromosomeEvaluator(temp_chromosome)
    temp_evaluator.print_evaluate_result()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"耗时: {elapsed_time:.6f}秒")
    input("...")