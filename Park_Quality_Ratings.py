import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

PIP_InspectionMain = pd.ExcelFile("InspectionMain.xlsx")
inspection = PIP_InspectionMain.parse()

PIP_FeatureRating = pd.ExcelFile("FeatureRatings.xlsx")
rating = PIP_FeatureRating.parse()

PIP_AllSites = pd.ExcelFile("ALLSITES.xlsx")
sites = PIP_AllSites.parse()

failedFeatures = rating[rating['Rating'].isin(['U'])]
badFeatures = rating[rating['Rating'].isin(['U/S'])]


# In[ ]:




# In[2]:

Inspections = {}

for feature in rating.iterrows():
    inspectionID = feature[1][2]
    featureRating =feature[1][1]
    
    if Inspections.get(inspectionID) == None:
        Inspections[inspectionID] = {'Count':0, 'Failures':0}
    
    if featureRating in ['U','U/S']:
        Inspections[inspectionID]['Failures']+=1
        
    Inspections[inspectionID]['Count']+=1


# In[ ]:




# In[7]:

Quality = {}
Ratio = 0

for key, value in Inspections.iteritems():
    if Quality.get(key) == None:
        Quality[key] = Ratio
    for item, score in value.iteritems():
        if item == 'Count':
            Count = score
        if item == 'Failures':
            Fail = score
    Ratio = float(Fail)/float(Count)


# In[8]:

parkInfo = {}
for feature in sites.iterrows():
    parkID = feature[1][1]
    borough = feature[1][2]
    district = feature[1][4]
    name = feature[1][6]
    acres = feature[1][9]
    category = feature[1][10]
    
    if parkInfo.get(parkID) == None:
        parkInfo[parkID] = {'Acres':0, 'Name':0, 'Borough':0, 'District':0, 'Category':0, 'Inpections':{}}
    parkInfo[parkID]['Acres']=float(acres)
    parkInfo[parkID]['Name']=name
    parkInfo[parkID]['Borough']=borough
    parkInfo[parkID]['District']=district
    parkInfo[parkID]['Category']=category


            
            #parkInfo[parkID]['Inpections']={inspectionID:{'Date':0,'Rating':0}}
    
    #if parkInfo.get(parkID) == None:
     #   pass
    #else:
       # if parkInfo[parkID] == parkID:
        #    parkInfo[parkID]['Inpections']={inspectionID:{'Date':0,'Rating':0}}
    #parkInfo[inspectionID]['Date']=date
    
    


# In[30]:

parkInspections = {}
import datetime
for feature in inspection.iterrows():
    parkID = feature[1][0]
    date = feature[1][3]
    inspectionID = feature[1][11]
    
    if parkInspections.get(parkID) == None:
        parkInspections[parkID] = {inspectionID:{'Date':date,'Rating':0}}
    #parkInspections[parkID][inspectionID]['Date']= date

    for key, value in Quality.iteritems():
        if inspectionID == key:
            parkInspections['Rating']=value
            

###
#for key, values in parkInfo.items():
 #   for feature in inspection.iterrows():
#      parkID = feature[1][0]
   #     date = feature[1][3]
    #    inspectionID = feature[1][11]    
     #   if key == parkID:
    #     parkInfo[parkID]['Inpections']={inspectionID:{'Date':0,'Rating':0}}
       #     print parkInfo


# In[31]:

#parkInspections


# In[9]:

#QualityRating = {}

#for feature in inspection.iterrows():
#    inspectionIDMaster = feature[1][11]
#    Date = feature[1][3]
#    Prop_ID = feature[1][0]

 #   if QualityRating.get(inspectionIDMaster) == None:
  #      QualityRating[inspectionIDMaster] = {'Prop_ID':0, 'Date':0, 'Rating':0, 'Area':0}
   # QualityRating[inspectionIDMaster]['Prop_ID']=Prop_ID
  #  QualityRating[inspectionIDMaster]['Date']=Date
#for key,value in Quality.iteritems():
    #for ID,values in QualityRating.iteritems():
      #  if key == ID:
        #    QualityRating[inspectionIDMaster]['Rating']=float(value)


# In[10]:

#for feature in sites.iterrows():
 #   Prop_ID = feature[1][2]
 #   featureRating =feature[1][1]


# In[11]:

#for key,value in Quality.iteritems():
   # for ID,values in QualityRating.iteritems():
     #   if key == ID:
       #     QualityRating[inspectionIDMaster]['Rating']=float(value)
            
            ""
