# -*- coding: utf-8 -*-
"""
@author: irene
"""

from time import time

from parsers import KnapsackSolverParser, DYNAMIC_PROGRAMMING_METHOD, SA_METHOD
from compare_test_results import compare_test_result
from dynamic_programming import KnapsackDynamicProgramming
from simulated_annealing import KnapsackSimulatedAnnealing

knapsack_method_factory = {DYNAMIC_PROGRAMMING_METHOD: KnapsackDynamicProgramming,
                           SA_METHOD: KnapsackSimulatedAnnealing
                           }

class KnapsackSolver:
    def __init__(self, parser):
        self.args = parser.parse_args()
        if self.args.method not in knapsack_method_factory:
            raise Exception("Unknown solving method")
        if self.args.method == SA_METHOD:
            if self.args.start_temperature < 1:
                raise Exception("Initial temperature for annealing approach must be at least 1")
            if self.args.min_temperature < 0:
                raise Exception("Minimum temperature for annealing approach must be greater than 0")
            if self.args.steps < 1:
                raise Exception("Number of steps for annealing approach iteration must be greater than 0")
        
    def solve(self):
        # repeating "repeat" time to get average solving time
        solving_time = 0
        for i in range(self.args.repeat):
            t_start = time()
            inst_num, sol_file, item_num = self.knapsack_solver()
            t_finish = time()
            solving_time += (t_finish - t_start)
        sol_file.write("Average solving time for each instance: %s\n" % (solving_time / self.args.repeat / inst_num))
        sol_file.close()
        print("Knapsack Solved. Average solving time: %ss (repetitions count %s, number of instances %s)" % (solving_time / self.args.repeat / inst_num, self.args.repeat, inst_num))
        if self.args.method != DYNAMIC_PROGRAMMING_METHOD and self.args.evaluate:
            compare_test_result(inst_num, item_num, self.args.method)
  
    def knapsack_solver(self):
        """Main method that solves knapsack problem using one of the existing methods"""
        inst_file = open(self.args.inst_file_path, "r")
        sol_file = open(self.args.inst_file_path.split('.')[0]+'_'+self.args.method+'_'+self.args.solution_file_path, "w")
    
        for line_no, line in enumerate(inst_file):
            inst_id, number, capacity, volume_value, item_available_qty = self.parse_line(line)
            method_solver = knapsack_method_factory[self.args.method](number, capacity, volume_value, item_available_qty)
            if not self.args.use_builtin and self.args.method == SA_METHOD:
                method_solver.init_temp = self.args.start_temperature
                method_solver.min_temp = self.args.min_temperature
                method_solver.steps = self.args.steps
            # get best value and the corresponding combination of items
            best_value, best_solution = 0, None
            for _ in range(3):
                v, s = method_solver.run()
                if v > best_value:
                    best_value, best_solution = v, s

#            print(best_value)
#            print(best_value, best_solution)
            best_solution_str = ",".join("%s" % i for i in best_solution)
            # write best result to file
            sol_file.write("%s,%s,%s,%s\n" % (inst_id, number, best_value, best_solution_str))
        
        if self.args.method == SA_METHOD: # record parameters
            sol_file.write('alpha: %s, init_temp: %s, min_temp: %s, steps: %s\n' % (method_solver.ALPHA, method_solver.init_temp, method_solver.min_temp, method_solver.steps))
    
        inst_file.close()
        return line_no + 1, sol_file, number
        
    def parse_line(self, line):
        """Line parser method
        :param line: line from input file
        :return: tuple like: (instance id, number of items, knapsack capacity,
                                list of tuples like: [(volume, value), (volume, value), ...])
        """
        parts = [int(value) for value in line.split()]
        inst_id, number = parts[0:2]
        capacity = parts[2:5]
        volume_value = [(parts[i:i+4]) for i in range(5, len(parts), 5)]
        item_available_qty = [(parts[i]) for i in range(9, len(parts), 5)]
        return inst_id, number, capacity, volume_value, item_available_qty

if __name__ == "__main__":
    solver = KnapsackSolver(KnapsackSolverParser())
    solver.solve()
