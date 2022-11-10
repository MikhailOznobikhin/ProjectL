# -*- coding: utf-8 -*-
import pandas as pd

path_to_result = 'D:/data/datasets/results/10_16.09.22.Listvyanka_pribrejna_23.08.2022/unique.csv'

df = pd.read_csv(path_to_result)

df['x'] = None
df['y'] = None

for i,r in df.iterrows():
    df.loc[i, 'x'] = r.x_y.split('_')[0]
    df.loc[i, 'y'] = r.x_y.split('_')[1]

df.to_csv('D:/data/datasets/results/10_16.09.22.Listvyanka_pribrejna_23.08.2022/unique1.csv')