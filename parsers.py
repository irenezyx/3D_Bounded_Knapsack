# -*- coding: utf-8 -*-
"""
@author: irene
"""

import argparse
import os

DP_METHOD = "dp"
SA_METHOD = "sa"

class KnapsackSolverParser(argparse.ArgumentParser):
    def __init__(self, description='Script solving the 3-D bounded knapsack problem'):
        super(KnapsackSolverParser, self).__init__(description=description)
        self.add_argument('-f', type=str, dest="inst_file_path", default=os.getcwd()+'/../input.csv',
                            help='Path to inst *.txt file')
#        self.add_argument('-o', type=str, dest="solution_file_path", default="output.txt",
#                            help='Path to file where solutions will be saved. Default value: output.txt')
        self.add_argument('-r', type=int, dest="repeat", default=1,
                            help='Number of repetitions. Default value: 1')
        self.add_argument("-m", default=SA_METHOD, type=str, dest="method",
                            choices=[DP_METHOD, SA_METHOD],
                            help="Solving method. Default value:  SA method")
        self.add_argument('-st', type=int, dest="start_temperature", default=50,
                            help='Initial temperature for annealing approach. Default value: 1500')
        self.add_argument('-mt', type=int, dest="min_temperature", default=1,
                            help='Minimum temperature for annealing approach. Default value: 0.01')
        self.add_argument('-n', type=int, dest="steps", default=100,
                            help='Number of steps for annealing approach iteration. Default value: 400')
        self.add_argument('-e', type=bool, dest="evaluate", default=False,
                            help='Flag for whether to evaluate the current method. Default value: True')
        self.add_argument('-ub', type=bool, dest="use_builtin", default=True,
                          help='Flag for whether to use the built in parameters. \
                          To specify parameters for algorithms, set False. Default value: True')
        self.add_argument('-d', type=bool, dest="debug_mode", default=False,
                            help='Set true to debug mode and use random generated testcases. Default value: False')