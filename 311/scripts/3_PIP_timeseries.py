
# coding: utf-8

# In[19]:

import pandas as pd
import os
get_ipython().magic(u'matplotlib inline')

PARQA = os.getenv('PARQA')


# In[15]:


def getAllFiles(path, frmt=None, full=False):
    '''return all files in the folder,
    filtered by format, if it was provided'''

    fs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if frmt!=None:
            fsTmp = [dirpath + '/' + fl for fl in filenames if fl.endswith(frmt)]
            fs.extend(fsTmp)
        else:
            fsTmp = filenames
            fs.extend(fsTmp)
    if full:
        return [path+f for f in fs]
    else:
        return fs

path = PARQA + 'data/PIP_TIMESERIES/11-01-2015'
scores = [x for x in getAllFiles(path,'.csv', False) if 'SpatialAggregated' in x]


# In[16]:

df = pd.DataFrame({score.split('/')[-4]:pd.read_csv(score, index_col='District')['Amenities & Area Normalized Score'] for score in scores})
df.head(4)


# In[26]:

df.transpose().plot(kind='line', 
                    figsize=(18,8), 
                    alpha=.6, 
                    title='Park District scores, normalised by area and amenities');


# In[17]:

df.to_csv(PARQA + 'data/PIP_Districts_timeseries.csv')

