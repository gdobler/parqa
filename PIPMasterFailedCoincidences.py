import pandas as pd
import sys

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

for feature in Features:
	print "%s: %d fails" % (feature, Features[feature]['Count'])
	for subFeature in Features[feature]['Failures']:
		print "\t%s:%.4f" % (subFeature, float(Features[feature]['Failures'][subFeature]) / Features[feature]['Count']) # ratio is printed
	print ""

