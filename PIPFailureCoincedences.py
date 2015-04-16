from sys import argv
import csv
import math

f = open(argv[1], 'rU')
myFile = csv.reader(f)

InspectionData = []
InspectionSummary = {}
InspectionItems = myFile.next()

for row in myFile:
	InspectionData.append(row)


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

for item in InspectionSummary:
	if item != "Inspection_Id":
		print "%s: %d fails" % (item, InspectionSummary[item]['Count']),
		for feature in InspectionSummary[item]:
			if feature != 'Count':
				print "\t%s:%d" % (feature, InspectionSummary[item][feature]),
		print ""
