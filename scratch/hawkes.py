#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy
#import tick
from tick import hawkes
import pandas as pd
import ncsr_import
import numpy as np
from tick.plot import plot_hawkes_kernels
import datetime

# In[2]:

#age_dates = pd.read_csv('age_init_as_dates.csv', index_col = 0)
#adj = pd.read_csv('all_adjacency_matrix.csv', index_col=0)
#age = pd.read_csv('justage_vars_init.csv', index_col=0)
#ncsr = ncsr_import.ncsr_data()
#age_mdd = pd.read_csv('age_mdd.csv', index_col=0)
#all_vars = pd.read_csv('all_vars_ncsr.csv', index_col=0)
pkl = open('../ncsr_for_ddp.pickle', "rb")

data = pickle.load(pkl)
pkl.close()


# ncsr_var_desc =  pd.DataFrame(columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])
# 
# for x in ncsr.root.iloc[:,0]:
#     ncsr_var_desc = ncsr_var_desc.append(ncsr.get_value_from_string(x))
# 
# ncsr_var_desc = ncsr_var_desc.reset_index(drop=True)
# ncsr_var_desc.to_csv("all_vars_ncsr.csv")

# In[3]:


# MDD is 3380

#mdd = ncsr.ncsr[ncsr.ncsr.iloc[:, 3380] == 1]


# In[4]:


#age_mdd = age_dates.iloc[mdd.index, :].reset_index(drop = True)


# In[5]:


#age_mdd.to_csv('age_mdd.csv')


# In[6]:


msk = np.random.rand(len(age_mdd)) < 0.02


# In[7]:


mdd_train = age_mdd[msk]
mdd_test = age_mdd[~msk]
current = 0
count = 0
for z, x in enumerate(mdd_train.values.tolist()): 
    count = 0
    current = z
    for y in x:
        try: 
            y = int(y)
        except: 
           y = y
        if y == -1:
            y = None
        else: 
            try: 
                y = datetime.datetime.strptime(y, "%m-%d-%Y")
                y = int(y.strftime('%Y%m%d'))
            except:
                y = y
        mdd_train.iloc[z, count] = y
        count += 1

    start_time = min([min(timestamp) for timestamp in event_timestamps])
    end_time = max([max(timestamp) for timestamp in event_timestamps])
    event_timestamps = [(timestamps-start_time).astype(int)/86400e9 for timestamps in event_timestamps]
 
    decays = [0.02,0.01,0.5]
    learner = HawkesSumExpKern(decays, penalty='elasticnet', elastic_net_ratio=0.8)
    learner.fit(event_timestamps)
 
    tracked_intensity, intensity_tracked_times = learner.estimated_intensity(event_timestamps,intensity_track_step=1/24.)
    estimated_intensity_index = start_time + pd.to_timedelta(intensity_tracked_times,unit='D')
    estimated_intensity = pd.DataFrame(np.vstack(tracked_intensity).T,index=estimated_intensity_index,columns=event_titles)
 
    return estimated_intensity

# In[8]:

#[x for x in mdd_train.values]

mdd_train = [ np.array(x) for x in mdd_train.values.tolist()]
#mdd_train = [int(x) for x in mdd_train]

# In[9]:


train_dim = len(mdd_train)
train_dim
mdd_train

# In[10]:


learner = hawkes.HawkesEM(train_dim,  n_threads=2, verbose = True, tol = 1e-3)


# In[ ]:


learner.fit(mdd_train)


# In[ ]:


plot_hawkes_kernels(learner)


# In[ ]:




