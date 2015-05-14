import pandas as pd
import geopandas as gp
import sys
import csv

# -- read data
filePath        = sys.argv[1]
filePath2       = sys.argv[2]

inspection      = pd.read_excel(filePath+"PIP_InspectionMain.xlsx")
parksProperties = gp.GeoDataFrame.from_file(filePath2+"Property.shp")

# -- pull off only first zip in list (if there are multiple)
parksProperties.ZIPCODE = parksProperties.ZIPCODE.apply(lambda x: x[:5])


# -- tack zip onto inspection data
inspection = pd.merge(inspection[inspection['Date'] \
                                     .apply(lambda x: x.year)==2014],
                      parksProperties[['GISPROPNUM','ZIPCODE']],
                      left_on='Prop ID', right_on='GISPROPNUM')


# -- only use actual inspections and convert "A"/"U" to 1/0
inspection = inspection[inspection['Overall Condition']!='N']
inspection['Overall Condition'] = inspection['Overall Condition'] \
                                     .apply(lambda x: 0 if x=="U" else 1)


# -- first group by property ID and determine if it failed in 2014, then group 
#    by zipcode and find the fraction of failures
ffrac = inspection.groupby('Prop ID')[['Overall Condition','ZIPCODE']].min() \
                           .groupby('ZIPCODE')['Overall Condition'] \
                           .apply(lambda x: (x==0).sum()/float(x.size)) \
                           .reset_index()
