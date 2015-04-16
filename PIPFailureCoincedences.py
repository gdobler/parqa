from sys import argv
import csv
import math

f = open(argv[1], 'rU')
myFile = csv.reader(f)
# headers = next(inspection)
# rating = headers.index("RATING")
# inspections_ID = headers.index("Inspections_Id")
# Insp_date = headers.index('Date')

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

print InspectionSummary


