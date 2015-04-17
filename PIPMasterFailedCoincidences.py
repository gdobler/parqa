import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

Inspections = {}
Features = {}

# IE. Features = {Ice: {Count:15, Failures: {Sidewalks:10, Playgrounds:12}}, 
#		  		  Litter: {Count:25, Failures: {Sidewalks:10, Playgrounds,14}}}

data = pd.ExcelFile(sys.argv[1])
df = data.parse()

# All failures
failedFeatures = df[df['Rating'].isin(['U'])]
# print failedFeatures

for feature in failedFeatures.iterrows():
	featureName = feature[1][0]
	inspectionID = feature[1][2]

	# Initialize Features in Master Dictionary
	if Features.get(featureName) == None:
		Features[featureName] = {'Count':0, 'Failures':{}}

	# Initialize Inspection in Master Inspection Dictionary
	if Inspections.get(inspectionID) == None:
		Inspections[inspectionID]= []

	# Increment Feature Count
	Features[featureName]['Count'] += 1

	# Add Feature to corresponding Inspection 
	Inspections[inspectionID].append(featureName)

for inspection in Inspections:
	# print inspection
	for i, feature in enumerate(Inspections[inspection]):
		for compareFeature in Inspections[inspection][i+1:]:
			if Features[feature]['Failures'].get(compareFeature) == None:
				Features[feature]['Failures'][compareFeature] = 0
			Features[feature]['Failures'][compareFeature] += 1

			if Features[compareFeature]['Failures'].get(feature) == None:
				Features[compareFeature]['Failures'][feature] = 0
			Features[compareFeature]['Failures'][feature] += 1

print Features

for feature in Features:
	print "%s: %d fails" % (feature, Features[feature]['Count'])
	for subFeature in Features[feature]['Failures']:
		print "\t%s:%.4f" % (subFeature, float(Features[feature]['Failures'][subFeature]) / Features[feature]['Count']) # ratio is printed
	print ""


fig, axs = plt.subplots(1,len(Features), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.001)
axs = axs.ravel()
i = 0
for mainFeature, details in Features.iteritems():
	for main, features in details.iteritems():
		if main != 'Count':
			axs[i].bar(range(len(features)), [float(x) / details['Count'] for x in features.values()], align='center', width=0.35)
			axs[i].set_xticks(np.arange(0, len(features)+1, 1.0))
			axs[i].set_xticklabels((details['Failures'].keys()),rotation=90)
			axs[i].set_ylim(0, 1)
			axs[i].set_title('%s, count of : %d'%(mainFeature, details['Count']))
			i+=1
fig.suptitle('Pecentages of Coincedences')
plt.show()


