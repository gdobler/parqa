import os
import numpy as np
import pandas as pd
import geopandas as gp

# -- initialize the output
fopen = open('../Outputs/unmatching.txt','w')

# -- read the inspection files
try:
    inspec
except:
    print("reading PIP_InspectionMain.xlsx...")
    in_path = os.path.join('../data','quality_assessment','PIP')
    in_name = os.path.join(in_path,'PIP_InspectionMain.xlsx')
    inspec  = pd.read_excel(in_name)


# -- create the base ID column
inspec['PID_base'] = [i.split('-')[0] for i in inspec['Prop ID']]


# -- read the full features file
featrat = pd.read_csv('../Outputs/transforms/PIP_FeatureRatings_transform.csv')


# -- check features file
check_FEATRAT = True
if check_FEATRAT:
    cnt = 0
    fopen.write('Inspection IDs found in PIP_InspectionsMain but not '
          'PIP_FeatureRatings:\n')
    for ii,iid in enumerate(inspec['Inspection ID']):
        if iid not in featrat['Inspection ID'].values:
#            print("couldn't find {0} : {1}".format(ii,iid))
            cnt +=1
            fopen.write("{0}\n".format(iid))
    fopen.write('Total: {0}\n'.format(cnt))

    fopen.write('\n# -------- \n\n')


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
check_ALLSITES = True
if check_ALLSITES:
#    print("checking allsites file...")
    fopen.write("Prop IDs found in PIP_InspectionMain but not PIP_ALLSITES:\n")
    cnt = 0
    missing = []
    for ii,pid in enumerate(inspec['Prop ID']):
        if pid not in allsites['Prop ID'].values:
#            print("couldn't find {0} : {1}".format(ii,pid))
            cnt += 1
            missing.append(pid)
    missing = set(missing)
    for miss in missing:
        fopen.write("{0}\n".format(miss))
    fopen.write('Total: {0}\n'.format(len(missing)))

    fopen.write('\n# -------- \n\n')


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
    fopen.write("Non-Greenstreet Prop IDs in InspectionsMain not found as " 
                "GISPROPNUMs in Property.shp:\n")
    cnt = 0
    missing = []
    for ii,pid in enumerate(inspec['PID_base']):
        if pid not in prop.GISPROPNUM.values:
            missing.append(pid)
            cnt += 1
    missing = set(missing)
    for miss in missing:
        fopen.write("{0}\n".format(miss))
    fopen.write('Total : {0}\n'.format(len(missing)))

    fopen.write('\n# -------- \n\n')


# -- merge the inspection and properties information
inspec = pd.merge(inspec, prop, 'left', left_on='PID_base', 
                  right_on='GISPROPNUM')


fopen.close()
