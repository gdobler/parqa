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

inspectionsDf = pd.read_excel(sys.argv[1])
locationsDf = pd.read_excel(sys.argv[2])
featuresDf = pd.read_excel(sys.argv[3])

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

	print '\n\nBOROUGH: %s\n\n' % boroughName
	for featureName, featureData in Features.items():
		print "%s: %d fails" % (featureName, featureData['Count'])
		for subFeatureName, subFeatureData in featureData['Failures'].items():
			print "\t%s:%.4f Count: %d, Evaluated: %d" % (subFeatureName, float(subFeatureData['Failures']) / subFeatureData['EvaluatedCount'], subFeatureData['Failures'], subFeatureData['EvaluatedCount']) # ratio is printed
		print ""


	# featuresList = [u'Litter', u'Athletic Fields', u'Lawns', u'Safety Surface', u'Trails', u'Weeds', u'Sidewalks', u'Ice', u'Glass', u'Benches', u'Paved Surfaces', u'Graffiti', u'Trees', u'Water Bodies', u'Play Equipment', u'Fences', u'Horticultural Areas']
	# newList = []
	# for index, feature in enumerate(featuresList):
	# 	newList.append([])
	# 	for i in featuresList:
	# 		if i == feature:
	# 			newList[index].append (1)
	# 		elif i == u'Weeds' and feature == u'Ice':
	# 			newList[index].append (0)
	# 		elif i == u'Safety Surface' and feature == u'Water Bodies':
	# 			newList[index].append (0)
	# 		elif i == u'Ice' and feature == u'Weeds':
	# 			newList[index].append (0)
	# 		elif i != feature:
	# 			newList[index].append (float(Features[feature]['Failures'][i]['Failures'])/Features[feature]['Failures'][i]['EvaluatedCount'])

	# newList = np.array(newList)
	# plt.imshow(newList, interpolation='nearest')
	# plt.xticks(range(17),featuresList, rotation='vertical')
	# plt.yticks(range(17),featuresList)
	# plt.colorbar()
	# plt.title('Coincidence Ratios of Failing Features')
	# plt.gcf().subplots_adjust(bottom=0.20)
	# plt.show()



