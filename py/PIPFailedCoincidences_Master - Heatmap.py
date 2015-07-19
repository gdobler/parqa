import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

Categories = { \
	'Cleanliness': [u'Glass', u'Graffiti', u'Ice', u'Litter', u'Weeds'], \
	'Structural' : [u'Benches', u'Fences', u'Paved Surfaces', u'Play Equipment', u'Safety Surface', u'Sidewalks'], \
	'Landscape' : [u'Athletic Fields', u'Horticultural Areas', u'Trails', u'Lawns', u'Trees', u'Water Bodies']}

Features = [u'Glass', u'Graffiti', u'Ice', u'Litter', u'Weeds', u'Benches', u'Fences', u'Paved Surfaces', u'Play Equipment', u'Safety Surface', u'Sidewalks', u'Athletic Fields', u'Horticultural Areas', u'Trails', u'Lawns', u'Trees', u'Water Bodies']

Boroughs = {'M': 'Manhattan', 'X': 'Bronx', 'Q': 'Queens', 'R': 'Staten Island', 'B': 'Brooklyn'}

def Replace3With1(Data):
	# -- Allows Dataframe used for other purposes to calculate Coincidence Failures as well.  U/S counted as '3' in dataframe.
	for Feature in Features:
		Data.loc[Data[Feature] == 3, Feature] = 1

def ReplaceBoroughs(Data):
	# -- Allows for labeling in plots
	for BKey, BFull in Boroughs.iteritems():
		Data.loc[Data['Boro'] == BKey, 'Boro'] = BFull

def NonCoincidenceFailure(Data, Spatial, MainFeature, SubFeature):
    
    MainInspected = Data[MainFeature].notnull()
    SubInspected = Data[SubFeature].notnull()
        
    DataSub = Data[MainInspected & SubInspected][[Spatial, MainFeature, SubFeature]]
    DataSubGroup = DataSub.groupby(Spatial)

    Count = DataSubGroup.count()[MainFeature]
    Failures = DataSubGroup.sum()[MainFeature]

    # Ratio of Main failing (while Sub still not null) over count of both existing together
    NonCoincidenceRatio = Failures.astype(float) / Count
    
    DataReturn = DataSubGroup.first().reset_index()[[Spatial]].set_index(Spatial)
    DataReturn['NonCoincidenceRatio'] = NonCoincidenceRatio
    DataReturn['OccuranceCount'] = Count

    return DataReturn


def CoincidenceFailure(Data, Spatial, MainFeature, SubFeature):
   
    MainInspected = Data[MainFeature].notnull()
    SubInspected = Data[SubFeature].notnull()
    SubFailed = Data[SubFeature] == 1
    
    DataSub = Data[MainInspected & SubInspected & SubFailed][[Spatial, MainFeature, SubFeature]]
    DataSubGroup = DataSub.groupby(Spatial)
    
    Count = DataSubGroup.count()[MainFeature]
    Failures = DataSubGroup.sum()[MainFeature]

    # Ratio of Both failing together over count of Main failing independently (while Sub still not null)
    CoincidenceRatio = Failures.astype(float) / Count
    
    DataReturn = DataSubGroup.first().reset_index()[[Spatial]].set_index(Spatial)
    DataReturn['CoincidenceRatio'] = CoincidenceRatio
        
    return DataReturn


def BuildRatios(df, Spatial):

	# -- Create DataFrame with Spatial as index
	CoincidenceRatios = df.groupby(Spatial).first().reset_index()[[Spatial]].set_index(Spatial)

    # -- For each MainFeature, compare it to all SubFeatures as long as they are not the same [CHANGED FOR SANITY CHECK TO EVEN COMPARE SAME]
	for MainFeature in Features:
		for SubFeature in Features:
			if MainFeature is not SubFeature:
               
	            # -- Call for Coincidence Ratio and NonCoincidence Ratios to be built and merged, indexed by Spatial
				CoincidenceCompare = pd.merge(CoincidenceFailure(df, Spatial, MainFeature, SubFeature), \
					NonCoincidenceFailure(df, Spatial, MainFeature, SubFeature), \
					left_index = True, \
					right_index= True, \
					how = 'outer')

				# -- Replace nulls with zeros to allow for Ratio subtraction. True nulls captured by the appending to CoincidenceRatios
				CoincidenceCompare.replace(to_replace=np.nan, value=0, inplace = True)
	            
				# -- Ratio desired is Coincidence - NonCoincidence (the average rate the MainFeature would have failed regardless of SubFeature failing)
				CoincidenceCompare['DesiredRatio'] = CoincidenceCompare['CoincidenceRatio'] - CoincidenceCompare['NonCoincidenceRatio']
	            
				CoincidenceRatios[MainFeature +'|'+ SubFeature] = CoincidenceCompare['DesiredRatio']

	return CoincidenceRatios



def FormatAndExport(Row):
	# -- Create Table with Features as index and columns
	ExportTable = pd.DataFrame(index=Features, columns=Features)

	# -- Place '1' on diagonals
	for Feature in Features:
		ExportTable.ix[Feature][Feature] = 1.0

	# Parse row info and place on DataFrame
	for Col in list(Row.index):
		[MainFeature, SubFeature] = Col.split('|')
		ExportTable.ix[MainFeature][SubFeature] = Row[Col]

	return ExportTable

def PlotHeatmap(df, SpatialItem, Path):

	plt.figure(figsize=(20, 20))
	newList = np.array(df).astype(float)
	cmap = plt.cm.seismic
	cmap.set_over('gray')
	plt.imshow(newList, interpolation='nearest',cmap=cmap, vmin=-.8,vmax=.8)	
	plt.xticks(range(17),Features, rotation='vertical')
	plt.yticks(range(17),Features)
	plt.colorbar()
	plt.title('%s Coincidence Ratios of Failing Features MINUS Average Rate of Failure' % SpatialItem)
	plt.xlabel('Coincidence Failing Feature')
	plt.ylabel('Main Failing Feature')
	plt.gcf().subplots_adjust(bottom=0.20)
	plt.savefig(Path + SpatialItem + '.png', bbox_inches='tight')
	
	# == Export DataFrames by Spatial
	# --Export Table to file
	out_filename = os.path.join(Path, '%s-RawData.csv' % (Spatial))
	df.to_csv(out_filename, sep=',', encoding='utf-8')

		


if __name__ == "__main__":
	# running with 'python fileName inputDataFrame outputPath Spatial'
	if len(sys.argv) == 4:
		SpatialKey = sys.argv[3]
		OutputPath = sys.argv[2]
		data = pd.DataFrame.from_csv(sys.argv[1], sep='\t')

		# -- Clean data
		data['NYC'] = 'NYC'
		Replace3With1(data)
		ReplaceBoroughs(data)

		if SpatialKey in data.columns:
			# -- Build Ratios against Spatial Key
			CompleteRawRatios = BuildRatios(data, SpatialKey)
			for Spatial, Row in CompleteRawRatios.iterrows():
				SpatialData = FormatAndExport(Row)
				PlotHeatmap(SpatialData, Spatial, OutputPath)

			# -- Plot data for entire dataset
			CompleteRawRatios = BuildRatios(data, 'NYC')
			for Spatial, Row in CompleteRawRatios.iterrows():
				SpatialData = FormatAndExport(Row)
				PlotHeatmap(SpatialData, Spatial, OutputPath)

		else:
			print '\nError: %s not found as valid attribute of %s' % (SpatialKey, sys.argv[1])
		
	else:
		print '\nError: Usage is: python %s <input_file> <output_path> <key_used_against_spatial_query>' % (sys.argv[0])
		print 'Example: python %s myDataFrame.csv myOutputFile.csv Boro' % (sys.argv[0])
else:
	print 'Imported: ' + sys.argv[0]

