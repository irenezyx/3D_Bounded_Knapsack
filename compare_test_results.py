# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 11:03:47 2019

@author: ZHANGYX
"""

from parsers import DYNAMIC_PROGRAMMING_METHOD, SA_METHOD
import pandas as pd

method_name_map = {DYNAMIC_PROGRAMMING_METHOD: 'Dynamic Programming',
                   SA_METHOD: 'Simulated Annealing'}

def compare_test_result(inst_num, number, method):
    """Compare method with the optimized solution provided by dynamic programming
    
        :param method: knapsack problem solving method
        :param number: number of items
    """
    sol_path = 'tests/test_' + str(number) + '_' + DYNAMIC_PROGRAMMING_METHOD + '_output.txt'
    check_path = 'tests/test_' + str(number) + '_' + method + '_output.txt'
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
            method_name_map[DYNAMIC_PROGRAMMING_METHOD]: ['100%', '0%', sol_time, ''],
            method_name_map[SA_METHOD]: ['{0}%'.format(acc), '{0}%'.format(err_size_rate), method_time, notes]}
    df = pd.DataFrame(data = data)
    print(df)
    df.to_csv('tests/test_compare_results/test_' + str(number) + '.csv')
    
if __name__ == '__main__':
    number = 30
    method = SA_METHOD
    inst_num = 50
    compare_test_result(inst_num, number, method)