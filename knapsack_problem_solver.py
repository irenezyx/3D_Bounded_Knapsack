# -*- coding: utf-8 -*-
"""
@author: irene
"""

import os
from time import time

from parsers import KnapsackSolverParser, DP_METHOD, SA_METHOD
from tests.compare_test_results import compare_test_result
from tests.generate_testcases import generate_tests
from GB.GBdata_transformer import transformers
from dynamic_programming import KnapsackDynamicProgramming
from simulated_annealing import KnapsackSimulatedAnnealing

knapsack_method_factory = {DP_METHOD: KnapsackDynamicProgramming,
                           SA_METHOD: KnapsackSimulatedAnnealing
                           }
truck_capacity = {'Transit': [236, 80, 108],
                  'E350': [240, 75, 84],
                  'Box Truck': [423, 103, 147],
                  'Platform': [422, 103, 106]
                  }
transit = 'Transit'
e350 = 'E350'
box_truck = 'Box Truck'
platform = 'Platform'

class KnapsackSolver:
    def __init__(self, parser, truck_type, rest_percent, in_jupyter = False):
        self.args = parser.parse_args()
        self.truck_type = truck_type
        self.transformer = transformers()
        self.rest_percent = rest_percent
        if in_jupyter:
            self.args.inst_file_path = os.getcwd()+'/../input.csv'
        if self.args.method not in knapsack_method_factory:
            raise Exception("Unknown solving method.")
        if self.args.method == SA_METHOD:
            if self.args.start_temperature < 1:
                raise Exception("Initial temperature for annealing approach must be at least 1.")
            if self.args.min_temperature < 0:
                raise Exception("Minimum temperature for annealing approach must be greater than 0.")
            if self.args.steps < 1:
                raise Exception("Number of steps for annealing approach iteration must be greater than 0.")
        if self.args.debug_mode:
            if not os.path.exists('tests/test_cases/test_30_10.txt'):
                generate_tests(30, 10, 'tests/test_cases/test_30_10.txt')
            self.args.inst_file_path = 'tests/test_cases/test_30_10.txt'
        else:
#            if not os.path.exists('GB/input.txt'):
            capacity = [truck_capacity[truck_type][i] * rest_percent[i] for i in range(3)]
#            print(self.args.inst_file_path)
            self.transformer.transform_to_input(self.args.inst_file_path, capacity)
            self.args.inst_file_path = 'GB/input.txt'
        
    def solve(self):
        # repeating "repeat" time to get average solving time
        solving_time = 0
        for i in range(self.args.repeat):
            t_start = time()
            inst_num, sol_file, item_num, best_value, best_solution = self.knapsack_solver()
            t_finish = time()
            solving_time += (t_finish - t_start)
        sol_file.write("Average solving time for each instance: %s\n" % (solving_time / self.args.repeat / inst_num))
        sol_file.close()
        print("Knapsack Solved. Average solving time: %ss (repetitions count %s, number of instances %s)" % (solving_time / self.args.repeat / inst_num, self.args.repeat, inst_num))
        
        if self.args.method != DP_METHOD and self.args.evaluate:
            sol_path = self.args.inst_file_path.split('.')[0]+'_'+self.args.method+'_output.txt'
            dp_sol_path = sol_path.split('_')
            dp_sol_path[-2] = DP_METHOD
            dp_sol_path = '_'.join(dp_sol_path)
            if os.path.exists(dp_sol_path):
                compare_test_result(inst_num, item_num, sol_path, dp_sol_path)
            else:
                print('To Evaluate, please run dynamic programming first.')
        return best_value, best_solution, self.transformer
  
    def knapsack_solver(self):
        """Main method that solves knapsack problem using one of the existing methods"""
        inst_file = open(self.args.inst_file_path, "r")
        sol_file = open(self.args.inst_file_path.split('.')[0]+'_'+self.args.method+'_output.txt', "w")
    
        for line_no, line in enumerate(inst_file):
            inst_id, number, capacity, volume_value, item_available_qty = self.parse_line(line)
            method_solver = knapsack_method_factory[self.args.method](number, capacity, volume_value, item_available_qty)
            if self.args.use_builtin and self.args.method == SA_METHOD:
                print('hahaha')
                method_solver.init_temp = self.args.start_temperature
                method_solver.min_temp = self.args.min_temperature
                method_solver.steps = self.args.steps
                perimeter = sum(truck_capacity[self.truck_type])
                if perimeter < 500:
                    method_solver.base_line = min(self.rest_percent) * perimeter * 8 # avoid bad values
                else:
                    method_solver.base_line = min(self.rest_percent) * perimeter * 7
                    
#            print(method_solver.base_line)
            best_value, best_solution = method_solver.run()

            best_solution_str = ",".join("%s" % i for i in best_solution)
            # write best result to file
            sol_file.write("%s,%s,%s,%s\n" % (inst_id, number, best_value, best_solution_str))
#            print(self.args.inst_file_path.split('.')[0]+'_'+self.args.method+'_output.txt')
        
        if self.args.method == SA_METHOD: # record parameters
            sol_file.write('alpha: %s, init_temp: %s, min_temp: %s, steps: %s\n' % (method_solver.ALPHA, method_solver.init_temp, method_solver.min_temp, method_solver.steps))
    
        inst_file.close()
        return line_no + 1, sol_file, number, best_value, best_solution
        
    def parse_line(self, line):
        """Line parser method
        :param line: line from input file
        :return: tuple like: (instance id, number of items, knapsack capacity,
                                list of tuples like: [(volume, value), (volume, value), ...])
        """
        parts = [float(value) if (i-5)%5==3 else int(value) for i, value in enumerate(line.split(','))]
#        parts = [float(value) for value in line.split(',')]
#        inst_id, number = list(map(int, parts[0:2]))
#        capacity = list(map(int, parts[2:5]))
#        volume_value = [(parts[i:i+4]) for i in range(5, len(parts), 5)]
#        for vv in volume_value:
#            vv[:3] = list(map(int, vv[:3]))
#        item_available_qty = [(parts[i]) for i in range(9, len(parts), 5)]
        inst_id, number = parts[0:2]
        capacity = parts[2:5]
        volume_value = [(parts[i:i+4]) for i in range(5, len(parts), 5)]
        item_available_qty = [(parts[i]) for i in range(9, len(parts), 5)]
        return inst_id, number, capacity, volume_value, item_available_qty

if __name__ == "__main__":
    rest_percent = [0.5] * 3
    solver = KnapsackSolver(KnapsackSolverParser(), platform, rest_percent)
    print(solver.solve())