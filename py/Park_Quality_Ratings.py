import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime

# Global Dictionarys
parkInfo = {}
Inspections = {}

PIP_InspectionMain = pd.ExcelFile("InspectionMain.xlsx")
inspection = PIP_InspectionMain.parse()

PIP_FeatureRating = pd.ExcelFile("FeatureRatings.xlsx")
rating = PIP_FeatureRating.parse()

PIP_AllSites = pd.ExcelFile("ALLSITES.xlsx")
sites = PIP_AllSites.parse()

failedFeatures = rating[rating['Rating'].isin(['U'])]
badFeatures = rating[rating['Rating'].isin(['U/S'])]

'''
Example Structures:

parkID = {<PARKID>: 
            {'Acres':0, 'Name':0, 'Borough':0, 'District':0, 'Category':0, 'Inpections':
                                                                                {<INSPECTIONID> : {'Count':0, 'Failures':0, 'Date':date, 'Rating':0}},
                                                                                {<INSPECTIONID> : {'Count':0, 'Failures':0, 'Date':date, 'Rating':0}},
                                                                                {<INSPECTIONID> : {'Count':0, 'Failures':0, 'Date':date, 'Rating':0}}
            }
          }



'''


#  Iterate through all inspection reports and sum Ratio of Failures of features to Features themselves.
#  Maintain 'Inspection' dictionary of format Inspection[<INSPECTIONID>]: {'Count':X, 'Failures':X}
for feature in rating.iterrows():
    inspectionID = feature[1][2]
    featureRating =feature[1][1]
    
    if Inspections.get(inspectionID) == None:
        Inspections[inspectionID] = {'Count':0, 'Failures':0}
    
    if featureRating in ['U','U/S']:
        Inspections[inspectionID]['Failures']+=1
        
    Inspections[inspectionID]['Count']+=1

'''
# Try this instead of above loop.  Might be more efficient.  Mostly just more 'python' like. :)
for inspectionID in pd.Series(sites[2]).unique():

  # Slice Inspection report
  InspectionDf = sites[sites[2] == inspectionID]

  # Create Masks
  RatingFilterU = InspectionDf[1] == 'U'
  RatingFilterUS = InspectionDf[1] == 'U/S'

  # Build Dictionary Entry
  Inspections[inspectionID] = {}
  Inspections[inspectionID]['Count'] = InspectionDf.count()
  Inspections[inspectionID]['Failures'] = InspectionDf[RatingFilterU | RatingFilterUS]
  Inspections[inspectionID]['Ratio'] = float(Inspections[inspectionID]['Failures']) / Inspections[inspectionID]['Count']
'''

for feature in sites.iterrows():
    parkID = feature[1][1]
    borough = feature[1][2]
    district = feature[1][4]
    name = feature[1][6]
    acres = feature[1][9]
    category = feature[1][10]
    
    if parkInfo.get(parkID) == None:
        parkInfo[parkID] = {'Inspections':{}}
    parkInfo[parkID]['Acres']=float(acres)
    parkInfo[parkID]['Name']=name
    parkInfo[parkID]['Borough']=borough
    parkInfo[parkID]['District']=district
    parkInfo[parkID]['Category']=category


for feature in inspection.iterrows():
    parkID = feature[1][0]
    date = feature[1][3]
    inspectionID = feature[1][11]

    '''  SEE if we can just read off the dataframe instead of going through the above for loop
    # Read entry 0... just in case there is more than one entry per parkID.. There shouldn't be regardless
    parkDfEntry = sites[sites[1] == parkID].ix[0]
    if parkDfEntry.empty:
      print 'No parkID matches %s found in Inspection file. SKIPPING inspectionID %s!' % (parkID, inspectionID)
    else:
      if parkInfo.get(parkID) == None:
          parkInfo[parkID] = {'Inpections':{}}
      
      parkInfo[parkID]['Acres']=float(parkDfEntry[1][9])
      parkInfo[parkID]['Name']=parkDfEntry[1][6]
      parkInfo[parkID]['Borough']=parkDfEntry[1][2]
      parkInfo[parkID]['District']=parkDfEntry[1][4]
      parkInfo[parkID]['Category']=parkDfEntry[1][10]

      IF USING ABOVE, INDENT BELOW!
          '''
      
    if parkInfo.get(parkID) == None:
      print 'Error: parkID %s not found in SITES file' % parkID
    elif Inspections.get(inspectionID) == None:
      print 'Error: inspectionID %s not found in FEATURERATING file' % inspectionID
    else:
      # Add inspection report to ParkID Dictionary
      parkInfo[parkID]['Inspections'][inspectionID] = Inspections[inspectionID]

      # Add inspection Date to Inspection sub Dictionary
      parkInfo[parkID]['Inspections'][inspectionID]['Date'] = date    # CHANGE TO DATETIME FORMAT!!!

      # !!!!!!   If Using commented out code from above, remove this section!
      # Create Ratio for inspection report and add to Inspection sub Dictionary
      inspectionFeatureCount = parkInfo[parkID]['Inspections'][inspectionID]['Count']
      inspectionFailureCount = parkInfo[parkID]['Inspections'][inspectionID]['Failures']
      parkInfo[parkID]['Inspections'][inspectionID]['Ratio'] = float(inspectionFailureCount)/inspectionFeatureCount
      

# Print a confirmation example of a park reference:
print parkInfo[parkID]
