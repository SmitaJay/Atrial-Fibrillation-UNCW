import pandas as pd
import numpy as np
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go
import graphviz
#from ncs1_import import ncs1_data
from ncsr_import import ncsr_data
import re
import copy
import pathpy as pp
import matplotlib.pyplot as plt
# For color mapping
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.lines as mlines
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

class ncsr_subject:
    
    def __init__(self, diagnosis1 = "", diagnosis2 = ""):
        self.ncsr_data = ncsr_data()
        self.ncsr_age = pd.read_csv('justage_vars_init.csv', index_col=0)
        self.diagnosis_1 = diagnosis1
        self.diagnosis_2 = diagnosis2
        self.edges = pd.DataFrame(0, columns = list(ncsr_age.columns)[1:], index=list(ncsr_age.columns)[1:])
        self.average_onset_age_init = {x: 0 for x in self.edges}

        

    def get_comorbid_subset(self, diagnosis1 = self.diagnosis_1, diagnosis2 = self.diagnosis_2):
        if diagnosis1 == "" or diagnosis2 ==  "":
            print("diagnosis1 & diagnosis2 must be set or passed into this function")
            return
        try:
            ncsr_age[diagnosis1]
            try: 
                ncsr_age[diagnosis2]
            except: 
                print("variable", diagnosis2, "does not exist in age variable subset \n\nSee extract_age_vars.py for more information")
                return
        except:
            print("variable", diagnosis2, "does not exist in age variable subset \n\nSee extract_age_vars.py for more information")
            return

        d1_subset = ncsr_age[(self.ncsr_data.ncsr.loc[:, diagnosis1] == 1)]
        d2_subset = ncsr_age[(self.ncsr_data.ncsr.loc[:, diagnosis2] == 1)]


        comorbid_subset_vals = [x for x in d1_subset.index if x in d2_subset.index]

        return d1_subset.loc[comorbid_subset_vals, :].reset_index(drop=True)

