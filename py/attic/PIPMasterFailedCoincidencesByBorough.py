import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv

Inspections = {}
BoroughFeatures = {}


# IE. Inspection = {IDNumber: [(Feature1, 1), (Feature2, 0)]}


# IE. Features = {Ice: {Count:15, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}, 
#		  		  Litter: {Count:25, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}}

# IE. BoroughFeatures = {'M': {Features},
#						 'B': {Features}}

inspectionsDf = pd.read_excel(sys.argv[1] + "PIP_InspectionMain.xlsx")
locationsDf = pd.read_excel(sys.argv[1] + "PIP_ALLSITES.xlsx")
featuresDf = pd.read_excel(sys.argv[1] + "PIP_FeatureRatings.xlsx")

inspectionsDfSub = inspectionsDf[['Inspection ID', 'Prop ID']]
locationsDfSub = locationsDf[['Prop ID', 'Boro']]

inspectionLocationDf = inspectionsDfSub.join(locationsDfSub.set_index(['Prop ID']), on='Prop ID')
featuresJoinedDf = featuresDf.join(inspectionLocationDf.set_index(['Inspection ID']), on='Inspection ID')


for feature in featuresJoinedDf[featuresJoinedDf['Boro'].notnull()].iterrows():
	featureName = feature[1][0]
	featureRating = feature[1][1]
	inspectionID = feature[1][2]
	borough = feature[1][5]

	# Initialize Features in Master Dictionary
	if featureRating in  ['U', 'U/S']:
		if BoroughFeatures.get(borough) == None:
			BoroughFeatures[borough] = {}
		
		if BoroughFeatures[borough].get(featureName) == None:
			BoroughFeatures[borough][featureName] = {'Count':0, 'Failures':{}}
			
		# Increment Feature Count
		BoroughFeatures[borough][featureName]['Count'] += 1

	# Initialize borough partition of Inspections
	if Inspections.get(borough) == None:
		Inspections[borough] = {}

	# Initialize Inspection in Master Inspection Dictionary
	if Inspections[borough].get(inspectionID) == None:
		Inspections[borough][inspectionID] = []

	# Add Feature to corresponding Inspection 
	Inspections[borough][inspectionID].append((featureName, featureRating))

for boroughName, boroughInspections in Inspections.items():

	# Initialize Features for each Borough
	Features = BoroughFeatures[boroughName]

	for inspectionNum, inspectionData in boroughInspections.items():
		for i, (featureName, featureRating) in enumerate(inspectionData):
			if featureRating in ['U','U/S']:

				for compareFeatureName, compareFeatureRating in inspectionData[i+1:]:

					# Initialize SubFeature
					if Features[featureName]['Failures'].get(compareFeatureName) == None:
						Features[featureName]['Failures'][compareFeatureName] = {'EvaluatedCount':0, 'Failures':0}

					# Increment Evaluated count regardless of that compared Feature's rating
					Features[featureName]['Failures'][compareFeatureName]['EvaluatedCount'] += 1

					# Increment Failed count if that compared Feature has a failed rating
					if compareFeatureRating in ['U','U/S']:
						Features[featureName]['Failures'][compareFeatureName]['Failures'] += 1

						if Features[compareFeatureName]['Failures'].get(featureName) == None:
							Features[compareFeatureName]['Failures'][featureName] = {'EvaluatedCount':0, 'Failures':0}
						Features[compareFeatureName]['Failures'][featureName]['EvaluatedCount'] += 1
						Features[compareFeatureName]['Failures'][featureName]['Failures'] += 1

	# print '\n\nBOROUGH: %s\n\n' % boroughName
	# for featureName, featureData in Features.items():
	# 	print "%s: %d fails" % (featureName, featureData['Count'])
	# 	for subFeatureName, subFeatureData in featureData['Failures'].items():
	# 		print "\t%s:%.4f Count: %d, Evaluated: %d" % (subFeatureName, float(subFeatureData['Failures']) / subFeatureData['EvaluatedCount'], subFeatureData['Failures'], subFeatureData['EvaluatedCount']) # ratio is printed
	# 	print ""

	featuresList = [u'Glass', u'Graffiti', u'Ice', u'Litter', u'Weeds', u'Benches', u'Fences', u'Paved Surfaces', u'Play Equipment', u'Safety Surface', u'Sidewalks', u'Athletic Fields', u'Horticultural Areas', u'Trails', u'Lawns', u'Trees', u'Water Bodies']
	boroughFullName = {'M': 'Manhattan', 'Q': 'Queens', 'X': 'Bronx', 'R': 'Staten Island', 'B': 'Brooklyn'}
	newList = []
	for index, feature in enumerate(featuresList):
		newList.append([])
		for i in featuresList:
			if i == feature:
				newList[index].append (1)
			elif i != feature:
				if Features[feature]['Failures'].get(i) == None:
					newList[index].append (100)
				else:
					newList[index].append (float(Features[feature]['Failures'][i]['Failures'])/Features[feature]['Failures'][i]['EvaluatedCount'])

	plt.figure(figsize=(20, 20))
	newList = np.array(newList)
	cmap = plt.cm.jet
	plt.imshow(newList, interpolation='nearest', cmap=cmap, vmin=0,vmax=1)
	cmap.set_over('gray')
	plt.xticks(range(17),featuresList, rotation='vertical')
	plt.yticks(range(17),featuresList)
	plt.colorbar()
	plt.title('%s Coincidence Ratios of Failing Features' % boroughFullName[boroughName])
	plt.xlabel('Coincidence Failing Feature')
	plt.ylabel('Main Failing Feature')
	plt.gcf().subplots_adjust(bottom=0.20)
	plt.savefig('../Outputs/Heatmaps/CoincidenceFailures/' + boroughName + '.png', bbox_inches='tight')
	



