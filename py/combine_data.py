import os
import numpy as np
import pandas as pd
import geopandas as gp

# -- read the inspection files
try:
    inspec
except:
    print("reading PIP_InspectionMain.xlsx...")
    in_path = os.path.join('../data','quality_assessment','PIP')
    in_name = os.path.join(in_path,'PIP_InspectionMain.xlsx')
    inspec  = pd.read_excel(in_name)


# -- create the base ID column
inspec['PID_base'] = [i.split('-')[0].replace('Z','') 
                      for i in inspec['Prop ID']]


# -- read the full features file
featrat = pd.read_csv('../Outputs/transforms/PIP_FeatureRatings_transform.csv')


# -- check features file
check_FEATRAT = False
if check_FEATRAT:
    for ii,iid in enumerate(inspec['Inspection ID']):
        if iid not in featrat['Inspection ID'].values:
            print("couldn't find {0} : {1}".format(ii,iid))


# -- combine inspections with detailed features
inspec = pd.merge(inspec,featrat,'left',on='Inspection ID')


# -- get all the sites information
try:
    allsites
except:
    print("reading PIP_ALLSITES.xlsx...")
    as_path  = os.path.join('../data','quality_assessment','PIP')
    as_name  = os.path.join(as_path,'PIP_ALLSITES.xlsx')
    allsites = pd.read_excel(as_name)


# -- check if there are inspected parks that aren't in allsites
check_ALLSITES = False
if check_ALLSITES:
    print("checking allsites file...")
    for ii,pid in enumerate(inspec['Prop ID']):
        flag = True
        for asid in allsites['Prop ID']:
            if pid==asid:
                flag = False
                break
        if flag:
            print("couldn't find {0} : {1}".format(ii,pid))


# -- merge ALLSITES Category with the inspection data
inspec = pd.merge(inspec,
                  allsites[['Prop ID','Category']] \
                      .groupby('Prop ID').first().reset_index(),
                  'left', on='Prop ID')


# -- remove Greenstreets
inspec = inspec[inspec.Category!='Greenstreet']


# -- read in the property files
try:
    prop
except:
    print("reading Property.shp...")
    pr_path = os.path.join('../Outputs','CUSPExportShps')
    pr_name = os.path.join(pr_path,'Property.shp')
    prop    = gp.GeoDataFrame.from_file(pr_name)


# -- check properties
check_PROP = True
if check_PROP:
    print("checking properties file...")
    pid_bad = []
    pid_bad_ii = []
    for ii,pid in enumerate(inspec['PID_base']):
        flag = True
        for gpn in prop.GISPROPNUM:
            if pid==gpn:
                flag = False
                break
        if flag:
            if pid not in pid_bad:
                pid_bad_ii.append(ii)
                pid_bad.append(pid)
            print("couldn't find {0} : {1}".format(ii,pid))

    for ii in range(len(pid_bad_ii)):
        subcat = allsites.iloc[allsites[allsites['Prop ID'] == \
                                inspec.iloc[pid_bad_ii[ii]]['Prop ID']] \
                                .index[0]]['Sub-Category']
        print("{0:8} : {1}" \
                  .format(inspec.iloc[pid_bad_ii[ii]]['Prop ID'],subcat))


# -- merge the inspection and properties information
inspec = pd.merge(inspec, prop, 'left', left_on='PID_base', 
                  right_on='GISPROPNUM')
