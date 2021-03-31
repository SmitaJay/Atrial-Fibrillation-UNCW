
import pandas as pd
import numpy as np
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go
import graphviz
from ncs1_import import ncs1_data
from ncsr_import import ncsr_data
import re
import copy
import pathpy as pp
#import matplotlib.pyplot as plt
# For color mapping
#import matplotlib.colors as colors
#import matplotlib.cm as cmx
#import matplotlib.lines as mlines
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
from tqdm import tqdm


# Pull ncsr data from file ncsr_import
ncsr = ncsr_data()
  # ncsr.ncsr holds all of the data from NCS 20240
  # https://www.icpsr.umich.edu/web/ICPSR/studies/20240
  # Alegria, Margarita, Jackson, James S. (James Sidney), Kessler, Ronald C., and Takeuchi, David. Collaborative Psychiatric Epidemiology Surveys (CPES), 2001-2003 [United States]. Ann Arbor, MI: Inter-university Consortium for Political and Social Research [distributor], 2016-03-23. https://doi.org/10.3886/ICPSR20240.v8
  # Key Functions:
    # ncsr.search_for_description looks for a descriotion of a column name in ncs1.dxdm or ncs1.survey
    # ncsr.get_variable_info queries icpsr for information like values, variable descriptions, and more
    # ncsr.get_value_from_string takes in a string that is a var name of dataframe in the ncsr description tree. Tree can be traversed using ncsr.root
  # Key Variables:
    # ncsr.ncsr 
    # ncsr.tree (Tree including descriptions of survey and dxdm columns)
    # ncsr.root (root used in traversing ncsr.tree)


# below code is used to cut out variables that have do do with onset age of symptoms
age_variable_subset = pd.DataFrame(columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])
#b = pd.DataFrame(columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])
#c = pd.DataFrame(columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])

for x in range(1, len(ncsr.root)):
    age_variable_subset = age_variable_subset.append(
        ncsr.get_value_from_string(ncsr.root.iloc[x,0])[
            np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*.*", False)) & np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*(^Age |^Age| age )+.*", False)) & np.logical_not(np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*(^Remember|^Exact|^Age$|#|biological|when you were born|^Freq)+.*", False)))
            ]
    )
   ##  this checks each regex to see the variables gut out. pd.concat below checks the difference between DFs
    #b = b.append(
   #     ncsr.get_value_from_string(ncsr.root.iloc[x,0])[
   #         np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])[
   #             'Description'].str.match(".*(first|1st|onset)+.*", False)) & np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])[
   #                 'Description'].str.match(".*(^Age |^Age| age | age|age | old|old | old |^DSM|^ICD)+.*", False))
   #         ]
   # )
   # c = c.append(
   #     ncsr.get_value_from_string(ncsr.root.iloc[x,0])[
   #         np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*(first|1st|onset)+.*", False))
   #         ]
   # )
   # pd.concat([,c]).drop_duplicates(keep=False).to_csv('out.csv')
#age_variable_subset = age_variable_subset.reset_index(drop=True)
age_variable_subset
#ncsr.ncs.to_csv('initialized_age_vars.csv')

ncsr_edges_init = pd.DataFrame(0, columns = age_variable_subset.iloc[:,0], index=age_variable_subset.iloc[:,0])

ncsr_subset = ncsr.ncsr[list(age_variable_subset.iloc[:, 0])]
# Go in and pull out the variables for a subject that are valid and in a 
for y in tqdm(range(0, len(ncsr_subset))):
    current_case = y
    case_age_vars = []
    for val, x in enumerate(age_variable_subset.iloc[:, 0]): 
            if ncsr_subset.loc[y, x] != ' ':
                if ncsr_subset.loc[y, x] != '.' and int(ncsr_subset.loc[y,x]) > 1 and int(ncsr_subset.loc[y,x]) < 100:
                    ncsr_subset.loc[y, x] = int(ncsr_subset.loc[y,x])
                else: 
                    ncsr_subset.loc[y, x] = 0
            else:
                ncsr_subset.loc[y,x] = 0

ncsr_subset.to_csv('age_subset.csv')
"""
average_onset_age_init = {}
for x in ncsr_edges_init:
    average_onset_age_init[x] = 0


ncsr_edges = ncsr_edges_init.copy(deep=True)
average_onset = copy.deepcopy(average_onset_age_init)
onset_count = copy.deepcopy(average_onset_age_init)
"""
"""
ncsr_graphs = []
for case in tqdm(range(len(ncsr_subset))):
    case_number = ncsr_subset.iloc[case, 0]
    ordered_vals =[]
    ordered_vars = []
    vals = []
    case_age_vars = []
    for symptom in ncsr_subset:
        if symptom != "CASEID":
            if ncsr_subset.loc[case, symptom] > 0:
                print(ncsr_subset.loc[case, symptom])
                vals.append(ncsr_subset.loc[case, symptom])
                case_age_vars.append(symptom)
    # initialize the ordered lists
    #order ints by age symptom occured
    for x in range(0, len(vals)):
        m = vals.index(min(vals))
        ordered_vals.append(vals[m])
        ordered_vars.append(case_age_vars[m])
        del vals[m]
        del case_age_vars[m]

    G = nx.DiGraph()
    for x in range(0, len(ordered_vals)):
        G.add_node(ordered_vars[x], age = ordered_vals[x])
    mult_flag = 0
    back_start = -1
    back_end = -1
    back_flag = 0
    start = 0
    for x in range(0, len(ordered_vars)-1):
        if ordered_vals[x] != ordered_vals[x+1]:
            if not mult_flag:
                G.ncsr_edges_from([(ordered_vars[x], ordered_vars[x+1])])
                back_flag = 0
            else: 
                for y in range(start, x+1):
                    G.ncsr_edges_from([(ordered_vars[y], ordered_vars[x+1])])
                    back_flag = 1
                    back_end = x
            back_start = start
            start = x + 1
            mult_flag = 0
        elif ordered_vals[x] == ordered_vals[x+1]:
            mult_flag = 1
            if back_start<0:
                continue
            if back_flag: 
                for y in range(back_start, back_end + 1):
                    G.ncsr_edges_from([(ordered_vars[y], ordered_vars[x+1])])
            else:
                G.ncsr_edges_from([(ordered_vars[back_start], ordered_vars[x+1])]) 

    ncsr_graphs.append(G)

for x in ncsr_graphs: 
    node_age_added = []
    for from_node in ncsr_subset.iloc[:,0]:
        for to_node in ncsr_subset.iloc[:,0]:
            if x.has_edge(from_node, to_node):
                if from_node not in node_age_added: 
                    onset_count[from_node] += 1
                    average_onset[from_node] += x.nodes[from_node]['age']
                    node_age_added.append(from_node)
                if to_node not in node_age_added:
                    onset_count[to_node] += 1
                    average_onset[to_node] += x.nodes[to_node]['age']
                    node_age_added.append(to_node)
                
                ncsr_edges.loc[from_node, to_node] += 1

for var, val in onset_count.items(): 
    if val > 0: 
        average_onset[var] = average_onset[var]/val

for x in range(len(ncsr_edges)):
    for y in range(len(ncsr_edges)):
        ncsr_edges.iloc[x, y] = ncsr_edges.iloc[x, y]/len(ncsr_subset)


ncsr_edges.to_csv("all_adjacency_matrix.csv")
"""