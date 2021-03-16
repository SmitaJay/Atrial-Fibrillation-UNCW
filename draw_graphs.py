import re
import pandas as pd
import json
import requests
import copy


class draw_graphs:
  # class to read in the ncs 06693 data & get it ready to use

  def __init__(self, ncs, ncsr_flag, dsm):
    self.ncs = copy.deepcopy(ncs)
    # ncs is dataTree from ncsr_import (ncsr_flag == 1) or ncs1_import (ncsr_flag == 0)
    self.ncsr_flag = ncsr_flag
    self.main_df = pd.read_csv('justage_vars_init.csv')
    self.age_vars = pd.read_csv('time_series_vars_ncsr-justage.csv')
    self.edge_df = pd.DataFrame(columns = age_vars.iloc[:,0], index=age_vars.iloc[:,0])
    self.dsm = dsm
    self.subset_df = pd.DataFrame()
    self.average_onset_age = {}
    self.node_occurence = {}
    for x in self.age_vars:
        self.average_onset_age[x] = 0

    for x in range(len(self.edge_df)):
        for y in range(len(self.edge_df)):
            self.edge_df.iloc[x, y] = 0

  def get_dsm_graph(self, dsm):
    # check that dsm val exists
    try: 
        self.ncs.columns.get_loc(dsm)
    except: 
        print("DSM Diagnosis " + dsm + "doesn't exist")
        return -1

    self.subset_df = get_dsm_df(dsm)

    a = copy.deepcopy(self.subset_df)
    a = a.iloc[:, 1:] >0
    for x in a:
        self.node_occurence[x] = eval("a." + x + ".sum()")/len(a.index)
    

  def get_dsm_df(self, dsm):
      return copy.deepcopy(self.main_df[self.main_df.loc[:, dsm] == 1].reset_index(drop=True))

  def get_individual_graph(self, caseID):
        graphs = []
        for case in range(len(self.sub)):
            case_number = add_subset.iloc[case, 0]
            ordered_vals =[]
            ordered_vars = []
            vals = []
            case_age_vars = []
            for symptom in add_subset:
                if symptom != "CASEID":
                    if add_subset.loc[case, symptom] > 0:
                        vals.append(add_subset.loc[case, symptom])
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
                        G.add_edges_from([(ordered_vars[x], ordered_vars[x+1])])
                        back_flag = 0
                    else: 
                        for y in range(start, x+1):
                            G.add_edges_from([(ordered_vars[y], ordered_vars[x+1])])
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
                            G.add_edges_from([(ordered_vars[y], ordered_vars[x+1])])
                    else:
                        G.add_edges_from([(ordered_vars[back_start], ordered_vars[x+1])]) 

            add_graphs.append(G)

        for x in add_graphs: 
            node_age_added = []
            for from_node in age_variable_subset.iloc[:,0]:
                for to_node in age_variable_subset.iloc[:,0]:
                    if x.has_edge(from_node, to_node):
                        if from_node not in node_age_added: 
                            onset_count[from_node] += 1
                            average_onset[from_node] += x.nodes[from_node]['age']
                            node_age_added.append(from_node)
                        if to_node not in node_age_added:
                            onset_count[to_node] += 1
                            average_onset[to_node] += x.nodes[to_node]['age']
                            node_age_added.append(to_node)
                        
                        add_edges.loc[from_node, to_node] += 1
      

  def list_dsm_diags(self):
    print(self.ncs.get_value_from_string(self.ncs.root.iloc[43,0]))



class dataTree : pass
  # ^ class to build our ncs1_data tree from. ncs1_data adds variables as necessary

class ncs1_data:
  # class that sets up description tree and holds all of our data
  def __init__(self):
    # initialize tree variables 
    # most important are dxdm,  survey, root, and tree
    self.tree_list = self.get_tree_list()
    self.ncs = ncs_tsv_parse()
    self.dxdm = self.ncs.dxdm
    self.survey = self.ncs.survey
    self.root = pd.DataFrame(columns = ['VarName', 'Description', 'Value', 'DataFrame', 'Start', 'End'])
    self.tree = dataTree()
    self.build_tree()

  def get_variable_info(self, var, dxdm_flag = -1):
    search_string = ""
    if dxdm_flag == -1: 
      try:
        self.survey.columns.get_loc(var)
        dxdm_flag = 0
      except:
        try:
          self.dxdm.columns.get_loc(var)
          dxdm_flag = 1
        except: 
          print("Variable " + var + " doesn't exist in the survey or DXDM")
          return
    
    if dxdm_flag == 0:
      search_string = 'https://pcms.icpsr.umich.edu/pcms/api/1.0/studies/06693/datasets/0001/variables/' + var
    else: 
      search_string = 'https://pcms.icpsr.umich.edu/pcms/api/1.0/studies/06693/datasets/0002/variables/' + var

    try:
      return requests.get(search_string).json()
    except: 
      print("Variable " + var + " didn't return a valid JSON from pcms.icpsr.umich.edu")
      return -1


  def get_value_from_string(self, var):
    # function to return next node from tree given the string
    try: 
      return eval("self.tree." + var)
    except:
      print("Value " + var + "not found in tree")
      return -1

  def search_for_description(self, var, dxdm_flag=-1, search_tree = pd.DataFrame(), lvl = 1, value = -99999999999999999):
    # function to search for a description of a column located in DS0001 or DS0002
    if search_tree.empty: 
      search_tree = self.root
      #initialize search_tree
    if dxdm_flag == -1:
      #initialize dxdm_flag
      try: 
        value = self.survey.columns.get_loc(var)
        dxdm_flag = 0
        search_tree = search_tree[search_tree.DataFrame == "survey"]
      except:
        try:
          value = self.dxdm.columns.get_loc(var)
          dxdm_flag = 2
          search_tree = search_tree[search_tree.DataFrame == "dxdm"]
        except:
          print("Value " + var + " not found in survey (DS0001) or dxdm (DS0002)")
          return
      search_tree = search_tree.reset_index(drop=True)
      for x in range(0, len(search_tree)):
        #find next node to enter
          if value <= search_tree.loc[x, 'End'] and value >= search_tree.loc[x, 'Start']:
              if search_tree.iloc[x, 0] != var:
                  return self.search_for_description(var, dxdm_flag, eval("self.tree." + str(search_tree.iloc[x,0])),  0, value)
              elif search_tree.iloc[x, 0] == var: 
                  return search_tree.iloc[x,:]
              else: 
                  return -1
    elif lvl == 1: 
        # initialize value when dxdm_flag is set
        if dxdm_flag: 
            try: 
                value = self.dxdm.columns.get_loc(var)
            except: 
                print("No value " + var + " in dxdm (DS0002)")
                return
            search_tree = search_tree[search_tree.DataFrame == "dxdm"]
        else: 
            try: 
                value = self.survey.columns.get_loc(var)
            except: 
                print("No value " + var + " in survey (DS0001)")
                return
            search_tree = search_tree[search_tree.DataFrame == "survey"]
        for x in range(0, len(search_tree)):
          # find next node to enter
            if value <= search_tree.iloc[x, 'End'] and value >= search_tree.iloc[x, 'Start']:
                if search_tree.iloc[x, 0] != var:
                  description = self.search_for_description(var, dxdm_flag, eval("self.tree." + search_tree.iloc[x,0]),  0, value)
                  return description
                elif search_tree.iloc[x, 0] == var: 
                    return search_tree.iloc[x,:]
                else: 
                    return -1
    else:
      # All values are initialized
        for x in range(0, len(search_tree)):
          # search for next node to enter
            if value <= search_tree.loc[x, 'End'] and value >= search_tree.loc[x, 'Start']:
              if search_tree.iloc[x, 0] != var and search_tree.loc[x, 'recursion_flag'] == 1:
                # recursion_flag makes sure that next node exists for recursion
                  return self.search_for_description(var, dxdm_flag, eval("self.tree." + search_tree.iloc[x,0]),  0, value)
              elif search_tree.iloc[x, 0] == var: 
                  return search_tree.iloc[x,:]
              else: 
                  return -1
    return -1

  def build_tree(self): 
    #This builds an object representing variable names and all of their desriptions. format is as follows: 
    # 1. root holds top level varnames & description & location in tree_list[] list
    # 2. tree.root.iloc[n, 0] holds the next level varnames, description, and either location in tree_list[] list or REF value if given
    # 3. tree.(tree.root.iloc[n,0]).iloc[n,0] varies. For some is is the final level with a 1D list with the column index from self.survey, for others it is the varname for another level
    # If this level exists it generally represents the final information 
    # To traverse the object: 
    # eval('tree.' + varnamestring)
    # LVL1 EX: eval('tree.' + root.iloc[4, 0])
    # LVL2 EX: eval('tree.' + eval('tree.' + root.iloc[4, 0] + ".iloc[0,0]"))
    for i in range(0, len(self.tree_list)):
        varname = re.sub('[^ A-Za-z0-9]+', '', self.tree_list[i][0])
        varname = re.sub('[ ]+', '_', varname)
          # Get Variable name
        if i <= 30:
          #all data for the questionnaire is in the first 30 sections
          start_end = self.get_tree_obj_array(varname, self.tree_list[i], 0)
          self.root.loc[len(self.root)] = [varname , self.tree_list[i][0], i, 'survey', start_end[0], start_end[1]]
            # Add info to root so that we can traverse object later
        else:
          start_end = self.get_tree_obj_array(varname, self.tree_list[i], 1)
          self.root.loc[len(self.root)] = [varname , self.tree_list[i][0], i, 'dxdm', start_end[0], start_end[1]]
            # Add info to root so that we can traverse object later

  def get_tree_obj_array(self, var, tl, dxdm_flag):
    # function used to turn self.root.tree from giant list to traversable object
    start = 10000000
    end = -10000000
      # initialize start & end to -10000000 so they throw errors if not changed
      # start & end used in search_for_description for easy search
    tmpDF = pd.DataFrame(columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])
      # recursion flag to know if there is another level of the root tree that holds variables
    for x in range(3, len(tl)):
        # starts at 3 because tree includes unused flags 
        if len(tl[x]) > 3: 
            # If List has sublists
            # All subtrees larger than 3 have sublists
            var2 = re.sub('[^ A-Za-z0-9]+', '', tl[x][0])
            var2 = re.sub('[ ]+', '_', var2)
              #Make sublist variable name by removing spaces and special characters
            start_end = self.get_tree_obj_array(var2, tl[x], dxdm_flag)
              # Recursively call function for next level
            if x == 3: 
                start = start_end[0]
                # first iteration gives start value
            if x+1 == len(tl):
                end = start_end[1]
                # last itereation gives end value
            if dxdm_flag: 
                tmpDF.loc[len(tmpDF)] = [var2, tl[x][0], var, start_end[0], start_end[1], 'dxdm', 1]
            else:
                tmpDF.loc[len(tmpDF)] = [var2, tl[x][0], var, start_end[0], start_end[1], 'survey', 1]
            # set row
        elif not dxdm_flag:
            #if dxdm flag is false it is the survey dataset DS0001
            if x == 3: 
                start = self.survey.columns.get_loc(tl[x][0])
                # first iteration gives start value
            if x+1 == len(tl):
                end = self.survey.columns.get_loc(tl[x][0])
            #start and end values are the the location of the varnames at 3 and the end of the list
               #^^^^ Find return values for parent node

            tmpDF.loc[len(tmpDF)] = [tl[x][0], tl[x][1], var, self.survey.columns.get_loc(tl[x][0]), self.survey.columns.get_loc(tl[x][0]), 'survey', 0]
            # iterate through list and add rows to df
        else:  
            # otherwise the values are part of the dxdm or DS0002 dataset
            if self.dxdm.columns.get_loc(tl[x][0]) < start: 
                start = self.dxdm.columns.get_loc(tl[x][0])
                # first iteration gives start value
            if self.dxdm.columns.get_loc(tl[x][0]) > end:
                end = self.dxdm.columns.get_loc(tl[x][0])
            #start and end values are the the location of the varnames at 3 and the end of the list
              #^^^^ Find return values for parent node

            tmpDF.loc[len(tmpDF)] = [tl[x][0], tl[x][1], var, self.dxdm.columns.get_loc(tl[x][0]), self.dxdm.columns.get_loc(tl[x][0]), 'dxdm', 0]
                # iterate through list and add rows to df
    
    tmpDF = pd.DataFrame(data = tmpDF, columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])

    setattr(self.tree, var, tmpDF)
    return (start, end)

