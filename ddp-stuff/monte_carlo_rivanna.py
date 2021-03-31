import numpy as np
import matplotlib
import pandas as pd
import random

time_vars = list(pd.read_csv('time_series_vars_ncs2.csv').iloc[:, 1])
edge_matrix = pd.DataFrame(0, columns=time_vars, index = time_vars)

for x in range(470890000):
    r1 = random.randint(0, len(time_vars)-1)
    r2 = random.randint(0, len(time_vars)-1)
    while r1 == r2: 
        r2 = random.randint(0, len(time_vars)-1)
    edge_matrix.loc[time_vars[r1], time_vars[r2]] +=1

edge_matrix.to_csv("monte_carlo_matrix.csv")