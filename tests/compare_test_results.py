# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 11:03:47 2019

@author: ZHANGYX
"""

import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from parsers import DP_METHOD, SA_METHOD
import pandas as pd

method_name_map = {DP_METHOD: 'Dynamic Programming',
                   SA_METHOD: 'Simulated Annealing'}

def compare_test_result(inst_num, number, check_path, sol_path):
    """Compare method with the optimized solution provided by dynamic programming
    
        :param method: knapsack problem solving method
        :param number: number of items
    """
    sol = []
    with open(sol_path, 'r') as sol_file:
        for line_no, line in enumerate(sol_file):
            if line_no == inst_num:
                sol_time = float(line.split(': ')[1])
            else:
                sol.append(float(line.split(',')[2]))
    to_check = []
    with open(check_path, 'r') as check_file:
        for line_no, line in enumerate(check_file):
            if line_no == inst_num + 1:
                method_time = float(line.split(': ')[1])
            elif line_no == inst_num:
                notes = line
            else:
                to_check.append(float(line.split(',')[2]))
        
    acc = 0 # the frequency of getting best value
    err_size_rate = 0 # the total err rate from best value
    
    for i in range(inst_num):
        if sol[i] == to_check[i]:
            acc += 1
        else:
            err_size_rate += (sol[i] - to_check[i]) / sol[i]
        
    # change acc and err into percentage
    acc = acc / inst_num * 100
    err_size_rate = err_size_rate * 100 / inst_num
    
    data = {'Algorithm': ['Accuracy', 'Average_Error_Rate', 'Average_Running_Time', 'Parameters'],
            method_name_map[DP_METHOD]: ['100%', '0%', sol_time, ''],
            method_name_map[SA_METHOD]: ['{0}%'.format(acc), '{0}%'.format(err_size_rate), method_time, notes]}
    df = pd.DataFrame(data = data)
    print(df)
    parts_of_check = check_path.split('/')
    if __name__ == '__main__':
        evaluation_results_path = 'test_compare_results/evaluate_' + parts_of_check[-1].split('.')[0] + '.csv'
    else:
        if parts_of_check[0] == 'tests':
            evaluation_results_path = 'tests/test_compare_results/test_' + str(number) + '_' + str(inst_num) + '_evaluate_' + parts_of_check[-1].split('.')[0] + '.csv'
        else:
            evaluation_results_path = '/'.join(parts_of_check[:-1])+'/evaluate.csv'
    df.to_csv(evaluation_results_path)
    
if __name__ == '__main__':
    number = 10
    inst_num = 1
    method = SA_METHOD
    check_path = 'test_cases/test_' + str(number) + '_' + str(inst_num) + '_' + method + '_output.txt'
    sol_path = 'test_cases/test_' + str(number) + '_' + str(inst_num) + '_' + DP_METHOD + '_output.txt'
    compare_test_result(inst_num, number, check_path, sol_path)