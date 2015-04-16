from sys import argv
import csv
import math
import matplotlib.pyplot as plt
import numpy as np

f = open(argv[1], 'rU')
myFile = csv.reader(f)

InspectionData = []
InspectionSummary = {}
InspectionItems = myFile.next()


# Creating a list of Arrays to llop through the data instead of looping through the file.
for row in myFile:
	InspectionData.append(row)


# Creating a dictionary of dctionaries where the key is one failing inspection feature
# at a time measured against the rest failing features -- measuring coincidence 
for i, item in enumerate(InspectionItems):
	InspectionSummary[item] = {'Count':0}
	for row in InspectionData:
		if row[i] == 'Unacceptable':
			InspectionSummary[item]['Count'] +=1
			for j, value in enumerate(row):
				if i != j and value == 'Unacceptable':
					if InspectionSummary[item].get(InspectionItems[j]) == None:
						InspectionSummary[item][InspectionItems[j]] = 1
					else:
						InspectionSummary[item][InspectionItems[j]] += 1


# Pretty Printing!
featureCounts = []
for item in InspectionSummary:
	if item != "Inspection_Id":
		print "%s: %d fails" % (item, InspectionSummary[item]['Count']),
		for feature in InspectionSummary[item]:
			featureCounts.append(InspectionSummary[item][feature])
			if feature != 'Count':
				print "\t%s:%d" % (feature, InspectionSummary[item][feature]),
		print ""




# Plotting Histograms
fig, axs = plt.subplots(1,len(InspectionSummary)-1, facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.001)
axs = axs.ravel()
yLimMax= max(featureCounts)
i = 0
for item, features in InspectionSummary.iteritems():
	if item != "Inspection_Id":
		axs[i].bar(range(len(features)), features.values(), align='center', width=0.35)
		axs[i].set_xticks(np.arange(0, len(features)+1, 1.0))
		axs[i].set_xticklabels((features.keys()),rotation=90)
		axs[i].set_ylim(0, yLimMax)
		axs[i].set_title(item)
		i+=1

fig.suptitle(argv[1])
plt.show()
