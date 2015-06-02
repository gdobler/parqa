import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime
import pickle as pkl
import os
import csv

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

def Read_Files(filePath):
  inspection = pd.read_excel(filePath + "PIP_InspectionMain.xlsx")
  rating = pd.read_excel(filePath + "PIP_FeatureRatings.xlsx")
  sites = pd.read_excel(filePath + "PIP_ALLSITES.xlsx")

def Build_Structures(filePath):

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


def AvgRatio(yearQueryList):
  AverageRatio = {}
  for parkName, parkData in parkInfo.items():
    count = 0
    ratioSum = 0
    for inspectionID, inspectionData in parkData['Inspections'].items():
      if inspectionData['Date'].year in yearQueryList:
        count += 1
        ratioSum += inspectionData['Ratio']
    if not count == 0:
      if parkName not in AverageRatio:
        AverageRatio[parkName] = (ratioSum/count)
      else:
        AverageRatio[parkName] = (AverageRatio[parkName]+(ratioSum/count))/2
  return AverageRatio
  print AverageRatio



if __name__ == '__main__':
  # Read Files.  Placing outside Build so accessible if interpretor left open after running script
  Read_Files(sys.argv[1])
  
  # If pickle file doesn't exist, build structure/file.  If does, read and ignore build.
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
