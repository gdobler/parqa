import os
import numpy as np
import pandas as pd
import geopandas as gp

def failure_fraction(year=2012):

    # -- read data 
    print("reading PIP_InspectionMain.xlsx...")
    in_path = os.path.join('../data','quality_assessment','PIP')
    in_name = os.path.join(in_path,'PIP_InspectionMain.xlsx')
    inspec  = pd.read_excel(in_name)

    print("reading Property.shp...")
    pr_path = os.path.join('../Outputs','CUSPExportShps')
    pr_name = os.path.join(pr_path,'Property.shp')
    prop    = gp.GeoDataFrame.from_file(pr_name)


    # -- pull off only first zip in list (if there are multiple)
    prop.ZIPCODE = prop.ZIPCODE.apply(lambda x: x[:5])


    # -- tack zip onto inspection data
    print("merging inspections with property data...")
    inspec = pd.merge(inspec[inspec['Date'].apply(lambda x: x.year)==year],
                      prop[['GISPROPNUM','ZIPCODE']],
                      left_on='Prop ID', right_on='GISPROPNUM')


    # -- only use actual inspections and convert "A"/"U" to 1/0
    inspec = inspec[inspec['Overall Condition']!='N']
    inspec['Overall Condition'] = inspec['Overall Condition'] \
        .apply(lambda x: 0 if x=="U" else 1)


    # -- first group by property ID and determine if it failed in
    #    2014, then group by zipcode and find the fraction of failures
    print("calculating failure fraction...")
    ffrac = inspec.groupby('Prop ID')[['Overall Condition','ZIPCODE']].min() \
        .groupby('ZIPCODE')['Overall Condition'] \
        .apply(lambda x: (x==0).sum()/float(x.size)) \
        .reset_index()

    return ffrac
