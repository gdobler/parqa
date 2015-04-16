import pandas as pd
import sys

Inspections = {}
Features = {}

# IE. Features = {Ice: {Count:15, Failures: {Sidewalks:10, Playgrounds:12}}, 
#		  		  Litter: {Count:25, Failures: {Sidewalks:10, Playgrounds,14}}}

data = pd.ExcelFile(sys.argv[1])
df = data.parse()

failedFeatures = df[df['Rating'].isin(['U'])]

for feature in failedFeatures:
	# Initialize Features in Master Dictionary
	if Features.get(feature['Feature']) == None:
		Features['Feature'] = {'Count':0, 'Failures:{}}

	# Initialize Inspection in Master Inspection Dictionary
	if Inspections.get(feature['Inspection_ID']) == None:
		Inspections['Inspection_ID']= []

	# Increment Feature Count
	Features['Feature']['Count'] += 1

	# Add Feature to corresponding Inspection 
	Inspections['Inspection_ID'].append(feature['Feature'])

for inspection in Inspections:
	for i, feature in enumerate(inspection):
		for compareFeature in inspection[i+1:]:
			if Features[feature]['Failures'].get(compareFeature) == None:
				Features[feature]['Failures'][compareFeature] = 0
			Features[feature]['Failures'][compareFeature] += 1

			if Features[compareFeature]['Failures'].get(feature) == None:
				Features[compareFeature]['Failures'][feature] = 0
			Features[compareFeature]['Failures'][feature] += 1

for feature in Features:
	print "%s: %d fails" % (feature, Features[feature]['Count']),
		for subFeature in Features[feature]['Failures']:
			print "\t%s:%d" % (subFeature, Features[feature]['Failures'][subFeature]),
		print ""

