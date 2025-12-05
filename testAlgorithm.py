import time

from GA_Algorithm import *

if __name__ == "__main__":

    # 测试功能===============================
    cruise_area = Area(0, 1, 0, 1)
    # target_area = Area(121.07, 121.65, 24.34, 24.98)
    # target_pos = Position(2.0, 0.5, 0.0)
    # temp_coord, temp_distance = BasicGeometryFunc.find_closet_coord_and_distance(cruise_area.generate_area_pos_list(), target_pos)
    # temp_distance_1 = BasicGeometryFunc.cal_distance_from_to_node(target_pos, cruise_area.center_pos)

    pos_A = Position(0.95, 0.5, 0.0)

    pos_B = Position(1.0, 0.0, 0.0)

    bearing_angle = BasicGeometryFunc.calculate_bearing_from_A_to_B(pos_A, pos_B)

    temp_distance_1 = BasicGeometryFunc.cal_distance_from_to_node(pos_A, pos_B)
    new_pos = BasicGeometryFunc.calculate_destination_haversine(pos_A, 90.0, temp_distance_1)

    result = BasicGeometryFunc.point_in_polygon_ray_casting(pos_A, cruise_area.generate_area_pos_list())


    # 测试通过==================================




    start_time = time.time()

    temp_scenario_generator = ScenarioGenerator()
    temp_scenario_generator.createScenario()

    #  temp_chromosome = Chromosome(temp_scenario_generator.red_side_list, temp_scenario_generator.blue_side_list)
    #  temp_chromosome.generate_chromosome_random()#
    #  temp_chromosome.print_chromosome()

    #  temp_evaluator = ChromosomeEvaluator()
    #  temp_evaluator.setupChromosome(temp_chromosome)
    #  temp_evaluator.evaluate()
    #  temp_evaluator.print_evaluate_result()

    # 新增变异的逻辑
    temp_ga_algorithm = GA_Algorithm()
    temp_ga_algorithm.setup(temp_scenario_generator, 100, 100)
    temp_ga_algorithm.initialize_chromosome()
    temp_ga_algorithm.loop()

    temp_ga_algorithm.best_chromosome.print_chromosome()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"耗时: {elapsed_time:.6f}秒")


    # 在找到最好的染色体后，再针对每一个打击方案分配发射车的位置，满足每个发射点间距1km，打击间隔时间不超过5秒
    # 思路是，先确定发射点，然后再调整时间。
    # 通过调用generate_detailed_launch_pos来计算每个发射车的位置和发射时间
    temp_ga_algorithm.best_chromosome.generate_detailed_launch_pos()

    input("...")