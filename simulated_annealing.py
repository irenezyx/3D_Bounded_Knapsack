# -*- coding: utf-8 -*-
"""
@author: irene
"""

import math
import random

from knapsack_constructor import KnapsackProblemConstructor

class KnapsackSimulatedAnnealing(KnapsackProblemConstructor):
    def __init__(self, number, capacity, volume_value, item_available_qty, init_temp=50, min_temp=1, steps=100, baseline=100):
        super(KnapsackSimulatedAnnealing, self).__init__(number, capacity, volume_value, item_available_qty)
        self.init_temp = init_temp
        self.min_temp = min_temp
        self.steps = steps        
        self.base_line = baseline
#        print(self.number, self.capacity, self.volume_value, self.item_available_qty)

    def run(self):
        ''' Kernel algo called by outside '''
        print(self.base_line)
        # control the speed of cooling
        if self.base_line > 6000:
            self.ALPHA = 0.99 
        elif self.base_line > 4000:
            self.ALPHA = 0.98
        elif self.base_line > 3000:
            self.ALPHA = 0.97
        else:
            self.ALPHA = 0.96
            
        best_value, best_solution = 0, None
        print(self.ALPHA)
        while best_value < self.base_line:
#            for _ in range(2):
            v, sol = self.simulate(self.init_solution())
            print(v)
            if v > best_value:
                best_value = v
                best_solution = sol
        print('run return')
        return best_value, best_solution

    def init_solution(self):
        """Used for initial solution(state) generation.
        By adding a random item while volume is less than self.capacity
        """    
        solution = [0] * self.number # qty for each item
        allowed_positions = list(range(self.number))
        cur_volume = [0] * 3
        while allowed_positions:
            idx = random.randint(0, len(allowed_positions) - 1)
            selected_position = allowed_positions.pop(idx)
            max_n = self.get_max_qty(selected_position, cur_volume)
            qty = random.randint(0, max_n)
            solution[selected_position] = qty
            cur_volume = self.get_value_and_volume_of_knapsack(solution)[1]
        return solution
    
    def get_max_qty(self, item_idx, cur_volume): 
        max_n = self.item_available_qty[item_idx]
        left_volume = [self.capacity[i]-cur_volume[i] for i in range(3)]
        for i in range(3):
            tmp = left_volume[i] // self.volume_value[item_idx][i]
            if tmp < max_n:
                max_n = tmp
        return max_n
    
    def get_value_and_volume_of_knapsack(self, solution):
        """Get value and volume of knapsack - fitness function
        """
        value, volume = 0, [0] * 3
        for item, qty in enumerate(solution):
            value += qty * self.volume_value[item][-1]
            for i in range(3):
                volume[i] += qty * self.volume_value[item][i]
        return value, volume
    
    def moveto(self, solution):
        """All possible moves are generated"""
        moves = []
        cur_value, cur_volume = self.get_value_and_volume_of_knapsack(solution)
        for i, cur_qty in enumerate(solution):
            if cur_qty < self.item_available_qty[i]:
                # check the left empty volume after add item i of qty 1
                rest_volume_i =  [self.capacity[di] - (self.volume_value[i][di] + cur_volume[di]) for di in range(3)]
                # add one qty for each item each time
                if all(di >= 0 for di in rest_volume_i):
                    move = solution[:]
                    move[i] += 1
                    moves.append(move)
            if cur_qty > 0:
                move = solution[:]
                move[i] -= 1
                if move not in moves:
                    moves.append(move)
        # print(moves)
        return moves
    
    
    def simulate(self, solution):
        """Simulated annealing approach for Knapsack problem"""
        temperature = self.init_temp
    
        best_sol = solution # [qty] of "self.number" self.number of items
        best_value = self.get_value_and_volume_of_knapsack(solution)[0]
    
        current_sol = solution
        while temperature >= self.min_temp:
#            current_value = self.get_value_and_volume_of_knapsack(best_sol)[0]
#            print('cur: ', current_value, current_sol)
            for _ in range(self.steps):
                moves = self.moveto(current_sol) # candidates list for next_move
                idx = random.randint(0, len(moves) - 1)
                random_move = moves[idx] # a random solution from candidates
                random_move_value = self.get_value_and_volume_of_knapsack(random_move)[0]
    #                print('random move value: ', random_move_value)
                delta_value = random_move_value - best_value
                if delta_value > 0:
                    best_sol = random_move
                    best_value = random_move_value
                    current_sol = random_move
                else:
                    if math.exp(delta_value / float(temperature)) > random.uniform(0, 1):
                        current_sol = random_move
    
            temperature *= self.ALPHA
#            print('temp: ', temperature)
#            if current_value >= best_value or temperature <= 0:
#                break
        return best_value, best_sol
