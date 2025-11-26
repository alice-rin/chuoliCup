import time

from Chromosome import *
from ScenarioGenerator import *

if __name__ == "__main__":
    start_time = time.time()

    temp_scenario_generator = ScenarioGenerator()
    temp_scenario_generator.createScenario()

    temp_chromosome = Chromosome(temp_scenario_generator.red_side_list, temp_scenario_generator.blue_side_list)
    temp_chromosome.generate_chromosome_random()
    temp_chromosome.print_chromosome()

    temp_evaluator = ChromosomeEvaluator(temp_chromosome)
    temp_evaluator.print_evaluate_result()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"耗时: {elapsed_time:.6f}秒")
    input("...")
