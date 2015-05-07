import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import copy

Inspections = {}
BoroughFeatures = {}


# IE. Inspection = {IDNumber: [(Feature1, 1), (Feature2, 0)]}


# IE. Features = {Ice: {OccuranceCount: 0, FailureCount:15, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}, 
#		  		  Litter: {OccuranceCount: 0, FailureCount:25, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}}

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
	if BoroughFeatures.get(borough) == None:
		BoroughFeatures[borough] = {}
	if BoroughFeatures[borough].get(featureName) == None:
		BoroughFeatures[borough][featureName] = {'OccuranceCount':0, 'FailureCount':0, 'Failures':{}}
	
	# Increment Occurance Count
	BoroughFeatures[borough][featureName]['OccuranceCount'] += 1
	
	# Increment Failure Count
	if featureRating in  ['U', 'U/S']:
		# Increment Feature Count
		BoroughFeatures[borough][featureName]['FailureCount'] += 1

	# Initialize borough partition of Inspections
	if Inspections.get(borough) == None:
		Inspections[borough] = {}

	# Initialize Inspection in Master Inspection Dictionary
	if Inspections[borough].get(inspectionID) == None:
		Inspections[borough][inspectionID] = []

	# Add Feature to corresponding Inspection 
	Inspections[borough][inspectionID].append((featureName, featureRating))

for boroughName, boroughInspections in Inspections.items():

	# Initialize Features for each Borough.  Copy so they can have own values
	CoincidenceFeatures = copy.deepcopy(BoroughFeatures[boroughName])
	NONCoincidenceFeatures = copy.deepcopy(BoroughFeatures[boroughName])

	for inspectionNum, inspectionData in boroughInspections.items():
		for i, (featureName, featureRating) in enumerate(inspectionData):

			# Check and build data against NonCoincidence data (Feature 2 fails when Feature 1 is included in inspection report either passing or failing)
			for compareFeatureName, compareFeatureRating in inspectionData[i+1:]:

				# Initialize SubFeature
				if NONCoincidenceFeatures[featureName]['Failures'].get(compareFeatureName) == None:
					NONCoincidenceFeatures[featureName]['Failures'][compareFeatureName] = {'EvaluatedCount':0, 'Failures':0}

				# Increment Evaluated count regardless of that compared Feature's rating
				NONCoincidenceFeatures[featureName]['Failures'][compareFeatureName]['EvaluatedCount'] += 1

				# Increment Failed count if that compared Feature has a failed rating
				if compareFeatureRating in ['U','U/S']:
					NONCoincidenceFeatures[featureName]['Failures'][compareFeatureName]['Failures'] += 1

				# Check whether reverse condition exists (Feature 1 fails when Feature 2 'exists' in inspection)
				if featureRating in ['U','U/S']:
					if NONCoincidenceFeatures[compareFeatureName]['Failures'].get(featureName) == None:
						NONCoincidenceFeatures[compareFeatureName]['Failures'][featureName] = {'EvaluatedCount':0, 'Failures':0}
					NONCoincidenceFeatures[compareFeatureName]['Failures'][featureName]['EvaluatedCount'] += 1
					NONCoincidenceFeatures[compareFeatureName]['Failures'][featureName]['Failures'] += 1


			if featureRating in ['U','U/S']:

				for compareFeatureName, compareFeatureRating in inspectionData[i+1:]:

					# Initialize SubFeature
					if CoincidenceFeatures[featureName]['Failures'].get(compareFeatureName) == None:
						CoincidenceFeatures[featureName]['Failures'][compareFeatureName] = {'EvaluatedCount':0, 'Failures':0}

					# Increment Evaluated count regardless of that compared Feature's rating
					CoincidenceFeatures[featureName]['Failures'][compareFeatureName]['EvaluatedCount'] += 1

					# Increment Failed count if that compared Feature has a failed rating
					if compareFeatureRating in ['U','U/S']:
						CoincidenceFeatures[featureName]['Failures'][compareFeatureName]['Failures'] += 1

						if CoincidenceFeatures[compareFeatureName]['Failures'].get(featureName) == None:
							CoincidenceFeatures[compareFeatureName]['Failures'][featureName] = {'EvaluatedCount':0, 'Failures':0}
						CoincidenceFeatures[compareFeatureName]['Failures'][featureName]['EvaluatedCount'] += 1
						CoincidenceFeatures[compareFeatureName]['Failures'][featureName]['Failures'] += 1	

	featuresList = [u'Glass', u'Graffiti', u'Ice', u'Litter', u'Weeds', u'Benches', u'Fences', u'Paved Surfaces', u'Play Equipment', u'Safety Surface', u'Sidewalks', u'Athletic Fields', u'Horticultural Areas', u'Trails', u'Lawns', u'Trees', u'Water Bodies']
	boroughFullName = {'M': 'Manhattan', 'Q': 'Queens', 'X': 'Bronx', 'R': 'Staten Island', 'B': 'Brooklyn'}
	newList = []
	for index, feature in enumerate(featuresList):
		newList.append([])
		for i in featuresList:
			if i == feature:
				newList[index].append (1)
			elif i != feature:
					# Neither features ever exist in the same inspection report, ever.
				if CoincidenceFeatures[feature]['Failures'].get(i) == None and NONCoincidenceFeatures[feature]['Failures'].get(i) == None:
					newList[index].append (100)

					# Features never fail together but feature 2 does fail when feature 1 passes sometimes.  Hence the Coincidence actually DECREASES likelihood of a failure. 
				elif CoincidenceFeatures[feature]['Failures'].get(i) == None:
					NonCoincidenceAvg = float(NONCoincidenceFeatures[feature]['Failures'][i]['Failures']) / NONCoincidenceFeatures[feature]['Failures'][i]['EvaluatedCount']
					newList[index].append (0 - NonCoincidenceAvg)

				else:
					#NonCoincidenceAvg = float(Features[feature]['FailureCount']) / Features[feature]['OccuranceCount']
					NonCoincidenceAvg = float(NONCoincidenceFeatures[feature]['Failures'][i]['Failures']) / NONCoincidenceFeatures[feature]['Failures'][i]['EvaluatedCount']
					CoincidenceAvg = float(CoincidenceFeatures[feature]['Failures'][i]['Failures']) / CoincidenceFeatures[feature]['Failures'][i]['EvaluatedCount']
					newList[index].append (CoincidenceAvg - NonCoincidenceAvg)
					# print 'CoincidenceAvg: %f, NonCoincidence: %f' % (NonCoincidenceAvg, CoincidenceAvg)

	plt.figure(figsize=(20, 20))
	newList = np.array(newList)
	cmap = plt.cm.seismic
	cmap.set_over('gray')
	plt.imshow(newList, interpolation='nearest',cmap=cmap, vmin=-1,vmax=1)	
	plt.xticks(range(17),featuresList, rotation='vertical')
	plt.yticks(range(17),featuresList)
	plt.colorbar()
	plt.title('%s Coincidence Ratios of Failing Features MINUS Average Rate of Failure' % boroughFullName[boroughName])
	plt.xlabel('Coincidence Failing Feature')
	plt.ylabel('Main Failing Feature')
	plt.gcf().subplots_adjust(bottom=0.20)
	plt.savefig('../Outputs/Heatmaps/CoincidenceMinusAvg/' + boroughName + '.png', bbox_inches='tight')
	



