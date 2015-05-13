import pandas as pd
import geopandas as gp 

#def Read_Files(filePath):
inspection = pd.read_excel(filePath+"PIP_InspectionMain.xlsx")
parksProperties = gp.GeoDataFrame.from_file(filePath2+"Property.shp")

zipPass = {}

for park in parksProperties.iterrows():
	ID = park[1][8]
	zipCode = park[1][23]
	zipCodeFive = zipCode[:5]
	if zipPass.get(zipCodeFive) == None:
		zipPass[zipCodeFive] = {'Failed':0, 'Count':0}
	for feature in inspection.iterrows():
	    parkID = feature[1][0]
	    year = feature[1][6]
	    passI = feature[1][7]
	    if year == "2014":
	    	if parkID == ID:
		    	if passI <> "A":
		    		zipPass[zipCodeFive]['Failed']+=1
		    	zipPass[zipCodeFive]['Count']+=1

filePath = Read_Files(sys.argv[1])
filePath2 = Read_Files(sys.argv[2])
