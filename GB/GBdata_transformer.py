# -*- coding: utf-8 -*-
"""
@author: irene
"""

import pandas as pd
import numpy as np
import random

class transformers:
    def __init__(self):
        self.item_gbid_map = {}

    def transform_solution(self, sol):
        chosen = []
        for i, qty in enumerate(sol):
            if qty > 0:
                gbid = self.item_gbid_map[i]
                row = self.df[self.df['Material'] == gbid]
                chosen.append([gbid, 
                               qty, 
                               str(row['Material Class'].values[0]),
                               float(row['GMR for Reporting'].values[0]),
                               float(row['Unit_profit'].values[0])
                              ])
        self.sol_df = pd.DataFrame(chosen, columns = ['GBID', 'Quantity', 'Material Class', 'GMR', 'Unit Profit'])
        return self.sol_df
    
    def transform_to_input(self, path, capacity):
        if path.split('.')[-1] != 'csv':
            raise Exception('The GB data file should be in csv format. Current: %s' % path)
        self.process_GBdata(path)
        gbid_list = list(self.df['Material'])
        input_txt = [0]
        for i, gbid in enumerate(gbid_list):
            self.item_gbid_map[i] = gbid
        input_txt.append(i+1)
        capacity = [int(c * 1000) for c in capacity]
        input_txt.extend(capacity)
        for gbid in gbid_list:
            item = self.df[self.df['Material']==gbid]
    #         print(item['Material'])
    #        input_txt.append(int(float(item['Length']) * 1000))
    #        input_txt.append(int(float(item['Width']) * 1000))
    #        input_txt.append(int(float(item['Height']) * 1000))
            input_txt.append(int(item['Length']))
            input_txt.append(int(item['Width']))
            input_txt.append(int(item['Height']))
            input_txt.append(float(item['Unit_profit']))
            input_txt.append(2000)
        input_txt = [str(item) for item in input_txt]
        input_txt = ','.join(input_txt)
    #    print(input_txt)
        with open('GB/input.txt', 'w') as f:
            f.write(input_txt)
    
    def process_GBdata(self, path):
        self.df = pd.read_csv(path).dropna()
    #    print('input self.df', self.df)
        self.df['Material'] = self.df['Material'].astype(np.int64)
        self.df['Unit_profit'] = self.df['Unit_profit'].astype(float)
        self.df['Height'] = (self.df['Height'].astype(float) * 1000).astype(np.int64)
        self.df['Length'] = (self.df['Length'].astype(float) * 1000).astype(np.int64)
        self.df['Width'] = (self.df['Width'].astype(float) * 1000).astype(np.int64)
        self.df = self.df[((self.df['Sum of Material Delivery Frequency in One D/h and Normal'] > 50) & 
                     (self.df['Unit_profit']> 0) & (self.df['GMR for Reporting'] > 0) &
                     (self.df['Length'] > 0) & (self.df['Width'] > 0) & (self.df['Height'] > 0) )]
        self.df = self.df.drop_duplicates()
        self.df['GMR_rank'] = self.df['GMR for Reporting'].rank(ascending=False)
        self.df['Profit_rank'] = self.df['Profit'].rank(ascending=False)
        weights = [(0.8, 0.2), (0.7, 0.3), (0.6, 0.4), (0.5, 0.5)]
        weight = random.sample(weights, 1)[0]
        self.df['rank'] = weight[0] * self.df['GMR_rank'] + weight[1] * self.df['Profit_rank']
        self.df = self.df.sort_values(by='rank').head(30)
#        print(len(self.df))