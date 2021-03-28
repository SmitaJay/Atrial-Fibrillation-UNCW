##############################################
"""
Georgia Smith
BSc Capstone Project
to_ddp_format.py

Deep Diffusion Process (DDP) is a RNN extension of the Hawkes Process for Point Processes
Takes data in the format:

train_data['train'][4][0:3] = [{'idx_event': 1,
  'type_event': 41,
  'time_since_start': 0.007577342664837768,
  'time_since_last_event': 0.007577342664837768,
  'time_since_last_same_event': 0.007577342664837768},
 {'idx_event': 2,
  'type_event': 36,
  'time_since_start': 0.008626435131835614,
  'time_since_last_event': 0.0010490924669978455,
  'time_since_last_same_event': 0.008626435131835614},
 {'idx_event': 3,
  'type_event': 31,
  'time_since_start': 0.008981700184589117,
  'time_since_last_event': 0.0003552650527535034,
  'time_since_last_same_event': 0.008981700184589117}]

justage_vars_init.csv includes all 9,282 subjects in NCSR w/ a subset of 308 age based variables and the 'CASEID' variable for identification

Code standardizes age varibles as a value between 0-1 by dividing age in years by 100
"""
##############################################

import pandas as pd
import numpy as np
#import networkx as nx
#from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
#import plotly.graph_objs as go
#import graphviz
#from ncs1_import import ncs1_data
from ncsr_import import ncsr_data
#import re
import copy
#import pathpy as pp
#import matplotlib.pyplot as plt
# For color mapping
#import matplotlib.colors as colors
#import matplotlib.cm as cmx
#import matplotlib.lines as mlines
#import pydot
#from networkx.drawing.nx_pydot import graphviz_layout
import pickle


ncsr = pd.read_csv('justage_vars_init.csv', index_col=0)
  #see extract_age_vars.py for the ncsr extraction




dpp_data = []


for x in ncsr.index: 
    sorted_case = ncsr.iloc[x, 1:].sort_values()
    sorted_vars = list(sorted_case.index)
    dpp_data.append([])
    count = 0 
    for y in range(len(sorted_case)):
        if sorted_case[y] != -1:
            dpp_data[x].append({})
            dpp_data[x][count]['type_event'] = list(ncsr.columns).index(sorted_vars[y])
            dpp_data[x][count]['time_since_start'] = sorted_case[y]/100
            count += 1


outfile = open("ncsr_for_ddp.pickle", "wb")
pickle.dump(dpp_data, outfile)
outfile.close()
   # data can be loaded with pickle.load(open('ncsr_for_ddp.pickle', "rb"))
