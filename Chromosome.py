import random

from sympy import false

from Node import *
from typing import List, Dict


class Chromosome:
    def __init__(self, red_launch_list: List[RedStrikeVehicleNode], blue_target_list: List[TargetNode]):
        self.red_launcher_list: List[RedStrikeVehicleNode] = []
        self.blue_target_list: List[TargetNode] = []

        self.node_action_dict: Dict[TargetNode, FireAction] = {}
        for vehicle in red_launch_list:
            temp_vehicle = vehicle.__copy__()
            self.red_launcher_list.append(temp_vehicle)
        for target in blue_target_list:
            temp_target = target.__copy__()
            self.blue_target_list.append(temp_target)

        self.sorted_target_list: List[TargetNode] = []

        self.is_the_best = false
        self.score = 0.0
        # 每一轮的最优胜的染色体不用变异，进入下一个迭代

    def __copy__(self):
        temp_chromosome = Chromosome(self.red_launcher_list, self.blue_target_list)


        # temp_chromosome.


    def generate_chromosome_random(self):
        self.node_action_dict.clear()
        self.sorted_target_list = sorted(self.blue_target_list, key=lambda x: x.price, reverse=True)
        for temp_target in self.sorted_target_list:
            self.find_feasible_missiles_by_rule1(temp_target)
            self.pick_and_assign_attack_missile_by_random(temp_target)

    def pick_and_assign_attack_missile_by_random(self, target_node: TargetNode):
        target_node.assigned_fire_action_list.clear()
        if len(target_node.feasible_fire_action_list) == 0:
            return
        # 这里的逻辑再修改一下
        # 首先对可行的feasible_fire_action_list打乱排序
        # 然后顺序遍历直到满足数量要求，那么就分配相应弹量
        # 在evolution步骤，再重新运行一次
        random.shuffle(target_node.feasible_fire_action_list)
        for temp_fire_action in target_node.feasible_fire_action_list:
            # 首先判断弹量是否满足
            if temp_fire_action.red_launcher_node.current_missile_num >= temp_fire_action.required_penetration_missile_num:

                temp_fire_action.assign_missile_num_by_damage_and_penetration()
                # 其实也就是 temp_fire_action.assigned_missile_num = temp_fire_action.required_penetration_missile_num
                temp_fire_action.red_launcher_node.current_missile_num = temp_fire_action.red_launcher_node.current_missile_num - temp_fire_action.assigned_missile_num
                target_node.assigned_fire_action_list.append(temp_fire_action)
                self.node_action_dict[target_node] = temp_fire_action
                return


    def unassign_attack_missile(self, target_node):
        for temp_fire_action in target_node.assigned_fire_action_list:
            temp_fire_action.red_launcher_node.current_missile_num += temp_fire_action.assigned_missile_num
            temp_fire_action.assigned_missile_num = 0

        target_node.assigned_fire_action_list.clear()

    def find_feasible_missiles_by_rule1(self, target: TargetNode):
        target.feasible_fire_action_list.clear()
        for temp_fire_node in self.red_launcher_list:
            temp_fire_action = FireAction(target, temp_fire_node, 0, 0)
            if temp_fire_action.check_feasibility_step_1() and temp_fire_action.cal_launch_time() and temp_fire_action.check_is_missile_number_required_meet():
                target.feasible_fire_action_list.append(temp_fire_action)
            else:
                continue
            # else:



    def print_chromosome(self):
        for target in self.blue_target_list:
            target_str = "Target: " + str(target.id) + "<-"
            missile_str = ""
            if len(target.assigned_fire_action_list) == 0:
                missile_str = "NULL"
            else:
                for temp_fire_action in target.assigned_fire_action_list:
                    missile_str += ("Launcher: " + str(temp_fire_action.red_launcher_node.id) +
                                    " Missile: " + str(temp_fire_action.red_launcher_node.missile.missile_type) +
                                    " number: " + str(temp_fire_action.assigned_missile_num) + ", ")
            print(target_str + missile_str)

    # 这个函数用于变异可行的基因，变异的的方式包括修改打击的弹的类型，数量。但是由于目前的题目中，打击弹的数量是根据目标定的，所以没有修改的空间。
    # 在完善毁伤模型之后才有修改弹量的意义
    # 此外
    def evolution(self, evolution_ratio:float):
        if evolution_ratio > 1.0:
            evolution_ratio = 1.0
        target_num = len(self.node_action_dict)
        num_to_select = min (round(evolution_ratio * target_num), target_num)

        selected_target_list = random.sample(list(self.node_action_dict.keys()), num_to_select)

        for temp_target in selected_target_list:
            self.unassign_attack_missile(temp_target)
            self.pick_and_assign_attack_missile_by_random(temp_target)


class ChromosomeEvaluator:

    def __init__(self):
        self.chromosome = None
        self.total_damage = 0.0
        self.total_cost = 0.0
        self.total_time = 0.0
        self.total_missile_number = 0.0
        self.score = 0.0
        # self.evaluate()

    def setupChromosome(self, chromosome: Chromosome):
        self.chromosome = chromosome

    def evaluate(self):
        if self.chromosome is None:
            return

        for target in self.chromosome.blue_target_list:
            for fire_action in target.assigned_fire_action_list:
                self.total_cost += fire_action.red_launcher_node.missile.price * fire_action.assigned_missile_num
                self.total_time = max(self.total_time, fire_action.launch_time)
                self.total_missile_number += fire_action.assigned_missile_num

            self.total_damage += target.price

        self.score = self.total_damage / self.total_cost # 20分钟

    def print_evaluate_result(self):
        print("总毁伤价值为： " + str(self.total_damage))
        print("总打击代价为： " + str(self.total_cost))
        print("总花费时间为： " + str(self.total_time))
        print("总使用弹量为： " + str(self.total_missile_number))