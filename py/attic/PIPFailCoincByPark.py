import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import copy

Inspections = {}
PropertyFeatures = {}


# IE. Inspection = {IDNumber: [(Feature1, 1), (Feature2, 0)]}


# IE. Features = {Ice: {OccuranceCount: 0, FailureCount:15, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}, 
#		  		  Litter: {OccuranceCount: 0, FailureCount:25, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}}


# IE. PropertyFeatures = {ParkID: {Features},
					  #ParkID: {Features}}

CategoryList = {'Cleanliness': [u'Glass', u'Graffiti', u'Ice', u'Litter', u'Weeds'],
				'Structural':[u'Benches', u'Fences', u'Paved Surfaces', u'Play Equipment', u'Safety Surface', u'Sidewalks'], 
				'Landscape': [u'Athletic Fields', u'Horticultural Areas', u'Trails', u'Lawns', u'Trees', u'Water Bodies']}



# Lookup Feature
FeatureCatDict = {}
for key, categories in CategoryList.items():
    for feature in categories:
        FeatureCatDict[feature] = key

inspectionsDf = pd.read_excel(sys.argv[1] + "PIP_InspectionMain.xlsx")
locationsDf = pd.read_excel(sys.argv[1] + "PIP_ALLSITES.xlsx")
featuresDf = pd.read_excel(sys.argv[1] + "PIP_FeatureRatings.xlsx")

inspectionsDfSub = inspectionsDf[['Inspection ID', 'Prop ID']]
locationsDfSub = locationsDf[['Prop ID', 'Boro', 'Category']]

inspectionLocationDf = inspectionsDfSub.join(locationsDfSub.set_index(['Prop ID']), on='Prop ID')
featuresJoinedDf = featuresDf.join(inspectionLocationDf.set_index(['Inspection ID']), on='Inspection ID')


for feature in featuresJoinedDf[featuresJoinedDf['Boro'].notnull()].iterrows():
	featureName = feature[1][0]
	featureRating = feature[1][1]
	inspectionID = feature[1][2]
	propertyID = feature[1][4]
	borough = feature[1][5]
	category = feature[1][6]

	# Initialize Features in Master Dictionary, Ignoring greenstreets!
	if category != 'Greenstreet':
		if PropertyFeatures.get(propertyID) == None:
			PropertyFeatures[propertyID] = {}
		if PropertyFeatures[propertyID].get(featureName) == None:
			PropertyFeatures[propertyID][featureName] = {'OccuranceCount':0, 'FailureCount':0, 'Failures':{}}
		
		# Increment Occurance Count
		PropertyFeatures[propertyID][featureName]['OccuranceCount'] += 1
		
		# Increment Failure Count
		if featureRating in  ['U', 'U/S']:
			# Increment Feature Count
			PropertyFeatures[propertyID][featureName]['FailureCount'] += 1

		# Initialize propertyID partition of Inspections
		if Inspections.get(propertyID) == None:
			Inspections[propertyID] = {}

		# Initialize Inspection in Master Inspection Dictionary
		if Inspections[propertyID].get(inspectionID) == None:
			Inspections[propertyID][inspectionID] = []

		# Add Feature to corresponding Inspection 
		Inspections[propertyID][inspectionID].append((featureName, featureRating))



# Make dataframe
CompleteDf = pd.DataFrame(columns = CategoryList.keys(), rows= PropertyFeatures.keys())


for propertyIDName, propertyInspections in Inspections.items():

	# Initialize Features for each Park.  Copy so they can have own values
	CoincidenceFeatures = copy.deepcopy(PropertyFeatures[propertyIDName])
	NONCoincidenceFeatures = copy.deepcopy(PropertyFeatures[propertyIDName])

	for inspectionNum, inspectionData in propertyInspections.items():
		for i, (featureName, featureRating) in enumerate(inspectionData):

			# Check and build data against NonCoincidence data (Feature 2 fails when Feature 1 is included in inspection report either passing or failing)
			for compareFeatureName, compareFeatureRating in inspectionData[i+1:]:

				# Make sure Features are in the same category
				if FeatureCatDict[featureName] is FeatureCatDict[compareFeatureName]:
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


			# Now check for Coincidences
			if featureRating in ['U','U/S']:

				for compareFeatureName, compareFeatureRating in inspectionData[i+1:]:

					# Only if category is the same
					if FeatureCatDict[featureName] is FeatureCatDict[compareFeatureName]:
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

	# Want to go through each feature in Category.  Sum Failure Ratios. Append DF.
	for Category, CategoryFeatures in CategoryList.items():
		CategoryRatioSum = 0
		NullCoincidenceCount = 0
		for feature in CategoryFeatures:
			for subfeature in CategoryFeatures:
				if subfeature != feature:
					# Neither features ever exist in the same inspection report, ever.
					if CoincidenceFeatures[feature]['Failures'].get(subfeature) == None and NONCoincidenceFeatures[feature]['Failures'].get(subfeature) == None:
						NullCoincidenceCount += 1

					# Features never fail together but feature 2 does fail when feature 1 passes sometimes.  Hence the Coincidence actually DECREASES likelihood of a failure. 
					elif CoincidenceFeatures[feature]['Failures'].get(i) == None:
						NonCoincidenceAvg = float(NONCoincidenceFeatures[feature]['Failures'][subfeature]['Failures']) / NONCoincidenceFeatures[feature]['Failures'][subfeature]['EvaluatedCount']
						CategoryRatioSum += (0 - NonCoincidenceAvg)

					else:
						NonCoincidenceAvg = float(NONCoincidenceFeatures[feature]['Failures'][subfeature]['Failures']) / NONCoincidenceFeatures[feature]['Failures'][subfeature]['EvaluatedCount']
						CoincidenceAvg = float(CoincidenceFeatures[feature]['Failures'][subfeature]['Failures']) / CoincidenceFeatures[feature]['Failures'][subfeature]['EvaluatedCount']
						CategoryRatioSum += (CoincidenceAvg - NonCoincidenceAvg)
						
		# Demoninator is the full grid of comparisons per category, minus the diagonals, minus any coincidences that never happened.
		CategoryCoincidenceCount = (len(CategoryFeatures) * len(CategoryFeatures)) - len(CategoryFeatures) - NullCoincidenceCount 
		CompleteDf[Category][propertyIDName] = float(CategoryRatioSum)/CategoryCoincidenceCount

CompleteDf.to_csv('../Outputs/Heatmaps/ParkLevelFailureRatios.csv')
	



