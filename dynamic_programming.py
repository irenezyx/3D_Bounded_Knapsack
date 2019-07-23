# -*- coding: utf-8 -*-
"""
@author: irene
"""
from knapsack_constructor import KnapsackProblemConstructor

class KnapsackDynamicProgramming(KnapsackProblemConstructor):
    def run(self):
        """
        Solve the bounded knapsack problem by finding the most valuable
        subsequence of `volume_value` subject that weighs no more than
        `capacity`.
    
        Solution from https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/
    
        :return: a pair whose first element is the sum of values in the best combination,
        and whose second element is the combination.
        """
        # dp[i][j][k] is going to store maximum value with knapsack capacity (i, j, k)
#        print(self.number, self.capacity, self.volume_value, self.item_available_qty)
#        print('dynamic running')
        self.capacity = [int(i) for i in self.capacity]
        max_i, max_j, max_k = self.capacity
        dp = [[[0] * (max_k+1) for _ in range(max_j+1)] for _ in range(max_i+1)]
        sol = [[[[0] * self.number for _ in range(max_k+1)] for _ in range(max_j+1)] for _ in range(max_i+1)]
        for i in range(max_i + 1):
            for j in range(max_j + 1):
                for k in range(max_k + 1):
#                    print(i, j, k)
                    for t in range(self.number): 
                        ti, tj, tk, t_value = map(int, self.volume_value[t])
                        if (ti <= i and tj <= j and tk <= k and sol[i-ti][j-tj][k-tk][t] < self.item_available_qty[t]): 
                            potential_value = dp[i-ti][j-tj][k-tk] + t_value
                            if potential_value > dp[i][j][k]:
                                dp[i][j][k] = potential_value
                                sol[i][j][k] = sol[i-ti][j-tj][k-tk][:] # return a new copy
                                sol[i][j][k][t] += 1
        return dp[max_i][max_j][max_k], sol[max_i][max_j][max_k]
    
