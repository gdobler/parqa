import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
import csv


Inspections = {}

Features = {}

# IE. Inspection = {IDNumber: [(Feature1, 1), (Feature2, 0)]}


# IE. Features = {Ice: {Count:15, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}, 
#		  		  Litter: {Count:25, Failures: {Sidewalks:{EvaluatedCount:10, Failures:10}, Playgrounds:{EvaluatedCount:10, Failures:10}}}}

data = pd.ExcelFile(sys.argv[1])
df = data.parse()


for feature in df.iterrows():
	featureName = feature[1][0]
	featureRating = feature[1][1]
	inspectionID = feature[1][2]

	# Initialize Features in Master Dictionary
	if featureRating in ['U','U/S']:
		if Features.get(featureName) == None:
			Features[featureName] = {'Count':0, 'Failures':{}}
			
		# Increment Feature Count
		Features[featureName]['Count'] += 1

		# Initialize Inspection in Master Inspection Dictionary
	if Inspections.get(inspectionID) == None:
		Inspections[inspectionID]= []

	# Add Feature to corresponding Inspection 
	Inspections[inspectionID].append((featureName, featureRating))

for inspection in Inspections:
	# print inspection
	for i, feature in enumerate(Inspections[inspection]):
		if feature[1] in ['U','U/S']:
			for compareFeature in Inspections[inspection][i+1:]:

				if Features[feature[0]]['Failures'].get(compareFeature[0]) == None:
					Features[feature[0]]['Failures'][compareFeature[0]] = {'EvaluatedCount':0, 'Failures':0}
				# Increment Evaluated count regardless of that compared Feature's rating
				Features[feature[0]]['Failures'][compareFeature[0]]['EvaluatedCount'] += 1
				# Increment Failed count if that compared Feature has a failed rating
				if compareFeature[1] in ['U','U/S']:
					Features[feature[0]]['Failures'][compareFeature[0]]['Failures'] += 1

					if Features[compareFeature[0]]['Failures'].get(feature[0]) == None:
						Features[compareFeature[0]]['Failures'][feature[0]] = {'EvaluatedCount':0, 'Failures':0}
					Features[compareFeature[0]]['Failures'][feature[0]]['EvaluatedCount'] += 1
					Features[compareFeature[0]]['Failures'][feature[0]]['Failures'] += 1


for feature in Features:
	print "%s: %d fails" % (feature, Features[feature]['Count'])
	for subFeature in Features[feature]['Failures']:
		differenceInEvaluated = Features[feature]['Failures'][subFeature]['EvaluatedCount'] - Features[feature]['Failures'][subFeature]['Failures']
		print "\t%s:%.4f Count: %d, Evaluated: %d" % (subFeature, float(Features[feature]['Failures'][subFeature]['Failures']) / Features[feature]['Failures'][subFeature]['EvaluatedCount'], Features[feature]['Failures'][subFeature]['Failures'], Features[feature]['Failures'][subFeature]['EvaluatedCount']) # ratio is printed
	print ""


featuresList = [u'Litter', u'Athletic Fields', u'Lawns', u'Safety Surface', u'Trails', u'Weeds', u'Sidewalks', u'Ice', u'Glass', u'Benches', u'Paved Surfaces', u'Graffiti', u'Trees', u'Water Bodies', u'Play Equipment', u'Fences', u'Horticultural Areas']
newList = []
for index, feature in enumerate(featuresList):
	newList.append([])
	for i in featuresList:
		if i == feature:
			newList[index].append (1)
		elif i != feature:
			if Features[feature]['Failures'].get(i) == None:
				newList[index].append (0)
			else:
				newList[index].append (float(Features[feature]['Failures'][i]['Failures'])/Features[feature]['Failures'][i]['EvaluatedCount'])

plt.figure(figsize=(20, 20))
newList = np.array(newList)
cmap = plt.cm.jet
plt.imshow(newList, interpolation='nearest',vmin=0,vmax=1)
cmap.set_over('gray')
plt.xticks(range(17),featuresList, rotation='vertical')
plt.yticks(range(17),featuresList)
plt.colorbar()
plt.title('Coincidence Ratios of Failing Features')
plt.xlabel('Coincidence Failing Feature')
plt.ylabel('Main Failing Feature')
plt.gcf().subplots_adjust(bottom=0.20)
# plt.savefig('foo.png',bbox_inches='tight')
plt.show()



##### Previous code for plotting
# fig, axs = plt.subplots(4,4, facecolor='w', edgecolor='k')
# fig.subplots_adjust(hspace = .5, wspace=.001)
# axs = axs.ravel()
# i = 0
# for mainFeature, details in Features.iteritems():
# 		for detailType, failureDetails in details.iteritems():
# 			if detailType != 'Count':
# 				print failureDetails
# 				print "++++++++++++"
# 			for InspectionFailure, EvCount in failureDetails.iteritems():
# 		if main != 'Count':
# 			axs[i].bar(range(len(features)), [float(x) / details['Count'] for x in features.values()], align='center', width=0.35)
# 			axs[i].set_xticks(np.arange(0, len(features)+1, 1.0))
# 			axs[i].set_xticklabels((details['Failures'].keys()),rotation=90)
# 			axs[i].set_ylim(0, 1)
# 			axs[i].set_title('%s, count of : %d'%(mainFeature, details['Count']))
# 			i+=1
# fig.suptitle('Pecentages of Coincedences')
# plt.show()


