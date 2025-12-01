from sqlalchemy.sql.operators import truediv

from Chromosome import *
from ScenarioGenerator import *

class GA_Algorithm:

    def __init__(self, temp_scenario_generator:ScenarioGenerator, chromosome_num:int, iter_num:int):

        self.red_side_list:List[RedStrikeVehicleNode] = temp_scenario_generator.red_side_list
        self.blue_side_list:List[TargetNode] = temp_scenario_generator.blue_side_list
        self.chromosome_list:List[Chromosome] = []

        self.chromosome_num:int = chromosome_num
        self.iter_num:int = iter_num

        self.best_chromosome:Chromosome = None
        self.best_score = 0.0

        self.chromosome_evaluator:ChromosomeEvaluator = ChromosomeEvaluator()

    def initialize_chromosome(self):

        self.chromosome_list.clear()

        for i in range(self.chromosome_num):
            temp_chromosome = Chromosome(self.red_side_list, self.blue_side_list)
            temp_chromosome.generate_chromosome_random()#
            self.chromosome_list.append(temp_chromosome)

    def loop(self):
        # 最多循环xx代

        # 如果循环20代，最优的分数是一样的，那么就停止
        same_score_count = 0
        same_score_break_num = 20

        last_best_score = 0.0

        for i in range(self.iter_num):
            # 先找到最好的染色体
            for temp_chromosome in self.chromosome_list:
                self.chromosome_evaluator.setupChromosome(temp_chromosome)
                self.chromosome_evaluator.evaluate()
                temp_chromosome.score = self.chromosome_evaluator.score
                temp_chromosome.is_the_best = False
                if self.best_score <= self.chromosome_evaluator.score:
                    self.best_score = self.chromosome_evaluator.score
                    self.best_chromosome = temp_chromosome


            self.best_chromosome.is_the_best = True
            # 然后 不是最好的染色体，都要进行变异

            for temp_chromosome in self.chromosome_list:
                # 后续可以根据分数再进行变异的参数调整
                if not temp_chromosome.is_the_best:
                    temp_chromosome.evolution(0.3)

            # 然后根据染色体评分进行染色体的排序，淘汰末尾的30%，由最好的30%进行补齐
            # 这部分功能先不写了
            # 因为染色体copy的功能写起来比较复杂，时间不够了，明天抽空再写


            print("loop number is: " + str(i) + " best score is: " + str(self.best_score))
            # 计数
            if last_best_score == self.best_score:
                same_score_count += 1
            else:
                same_score_count = 0
            if same_score_count>= same_score_break_num:
                return

            last_best_score = self.best_score

