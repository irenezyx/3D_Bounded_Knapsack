# -*- coding: utf-8 -*-
"""
@author: irene
"""

import random
import os

def generate_tests(number=50, inst_num=50, path=''):
    if not path:
        path = 'test_cases/test_' + str(number) + '_' + str(inst_num) + '.txt'
    print(os.getcwd())
    inst_file = open(path, 'w')
    for i in range(inst_num):
        capacity = [random.randint(50, 200) for _ in range(3)]
        volume_value_availability = []
        for n in range(number):
            volume_value_availability.extend([random.randint(1, 50) for _ in range(3)])
            volume_value_availability.append(random.randint(1, 100))
            volume_value_availability.append(random.randint(500, 2500))
        inst_file.write("%s,%s,%s,%s\n" % (i, number, ','.join(map(str, capacity)), 
                                              ','.join(map(str, volume_value_availability))))
    inst_file.close()
    print('Finish generating random testcases in file \'%s\' with %s instances, each with %s items.' % (path, inst_num, number))
    
if __name__ == '__main__':
    generate_tests(number=10, inst_num=1)