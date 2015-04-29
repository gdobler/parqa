import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime
import pickle as pkl
import os

# Global Dictionarys
parkInfo = {}
Inspections = {}

# DAT File
datFile = 'parkInfo.pkl'
datFilePath = '../.dat/'

'''
Example Structures:
parkID = {<PARKID>: 
            {'Acres':0, 'Name':0, 'Borough':0, 'District':0, 'Category':0, 'Inspections':
                                                                                {<INSPECTIONID> : {'Count':0, 'Failures':0, 'Date':date, 'Rating':0}},
                                                                                {<INSPECTIONID> : {'Count':0, 'Failures':0, 'Date':date, 'Rating':0}},
                                                                                {<INSPECTIONID> : {'Count':0, 'Failures':0, 'Date':date, 'Rating':0}}
            }
          }
'''

def Build_Structures(filePath):

  inspection = pd.read_excel(filePath + "PIP_InspectionMain.xlsx")
  rating = pd.read_excel(filePath + "PIP_FeatureRatings.xlsx")
  sites = pd.read_excel(filePath + "PIP_ALLSITES.xlsx")

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

      if parkInfo.get(parkID) == None:
        print 'Error: parkID %s not found in SITES file' % parkID
      elif Inspections.get(inspectionID) == None:
        print 'Error: inspectionID %s not found in FEATURERATING file' % inspectionID
      else:
        # Add inspection report to ParkID Dictionary
        parkInfo[parkID]['Inspections'][inspectionID] = Inspections[inspectionID]

        # Add inspection Date to Inspection sub Dictionary
        parkInfo[parkID]['Inspections'][inspectionID]['Date'] = date    # CHANGE TO DATETIME FORMAT!!!

        # Create Ratio for inspection report and add to Inspection sub Dictionary
        inspectionFeatureCount = parkInfo[parkID]['Inspections'][inspectionID]['Count']
        inspectionFailureCount = parkInfo[parkID]['Inspections'][inspectionID]['Failures']
        parkInfo[parkID]['Inspections'][inspectionID]['Ratio'] = float(inspectionFailureCount)/inspectionFeatureCount


def AvgRatio(yearQueryList, CategoryList):
  AverageRatio = []
  for parkName, parkData in parkInfo.items():
    if parkData['Category'] in CategoryList:
      count = 0
      ratioSum = 0
      for inspectionID, inspectionData in parkData['Inspections'].items():
        if inspectionData['Date'].year in yearQueryList:
          count += 1
          ratioSum += inspectionData['Ratio']
      if not count == 0:
        AverageRatio.append(ratioSum/count)
  return AverageRatio




if __name__ == '__main__':

  if not os.path.exists(datFilePath + datFile):
      print 'Data File not found.  Building'
      Build_Structures(sys.argv[1])
      if not os.path.exists(datFilePath):
        os.makedirs(datFilePath)
      fopen = open(datFilePath + datFile, 'wb')
      pkl.dump(parkInfo,fopen)
      fopen.close()
  else:
    fopen = open(datFilePath + datFile, 'rb')
    parkInfo = pkl.load(fopen)
    fopen.close()

  # Call Average Ratio with all Categories
  Complete2014Ratios = AvgRatio([2014], ['Green Street', 'Large Park', 'Small Park'])
  Subset2014Ratios = AvgRatio([2014], ['Large Park', 'Small Park'])

  print Complete2014Ratios

