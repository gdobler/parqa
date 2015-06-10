import os
import sys
import numpy as np
import pandas as pd

# -- read the full features file
try:
    featrat
except:
    print("reading PIP_FeatureRatings.xlsx...")
    fr_path = os.path.join('../data','quality_assessment','PIP')
    fr_name = os.path.join(fr_path,'PIP_FeatureRatings.xlsx')
    featrat = pd.read_excel(fr_name)


# -- get the full set of features and columns
cols = ['Inspection ID'] + np.sort(list(set(featrat['Feature']))).tolist()


# -- initialize an empty data frame
iids      = list(set(featrat['Inspection ID']))
nind      = len(iids)
featxform = pd.DataFrame(index=iids,columns=cols)


# -- fill the columns
print("filling new dataframe...")

featxform['Inspection ID'] = np.sort(iids)

for ii,iid in enumerate(iids):
    if (ii+1)%100==0:
        print("{0} of {1}\r".format(ii+1,nind)),
        sys.stdout.flush()

    indices = np.arange(len(featrat))[(featrat['Inspection ID']==iid) \
                                          .as_matrix()]

    for index in indices:
        feat = featrat.iloc[index].Feature
        rat  = featrat.iloc[index].Rating
        featxform.ix[iid,feat] = rat

featxform.reset_index(inplace=True, drop=True)


# -- write to file
featxform.to_csv('../Outputs/transforms/PIP_FeatureRatings_transform.csv')
