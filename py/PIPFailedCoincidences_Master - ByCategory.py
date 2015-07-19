import pandas as pd
import numpy as np
import sys

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


def BuildRatios(df, outputFile):

	# -- Create DataFrame with SpatialKey as index
	CoincidenceRatios = df.groupby(SpatialKey).first().reset_index()[[SpatialKey]].set_index(SpatialKey)

	# -- For each Category, build seperate Ratio and Counts of all feature comparisons
	for CategoryName, CategoryValues in Categories.iteritems():

	    CategoryRatios = df.groupby(SpatialKey).first().reset_index()[[SpatialKey]].set_index(SpatialKey)
	    CategoryCounts = df.groupby(SpatialKey).first().reset_index()[[SpatialKey]].set_index(SpatialKey)

	    # -- For each MainFeature, compare it to all SubFeatures as long as they are not the same
	    for MainFeature in CategoryValues:
	        for SubFeature in CategoryValues:
	            if MainFeature is not SubFeature:
	               
	                # -- Call for Coincidence Ratio and NonCoincidence Ratios to be built and merged, indexed by Spatial
	                CoincidenceCompare = pd.merge(CoincidenceFailure(df, SpatialKey, MainFeature, SubFeature), \
	                            NonCoincidenceFailure(df, SpatialKey, MainFeature, SubFeature), \
	                            left_index = True, \
	                            right_index= True, \
	                            how = 'outer')
	                
	                # -- Replace nulls with zeros to allow for Ratio subtraction. True nulls captured by the appending to CoincidenceRatios
	                CoincidenceCompare.replace(to_replace=np.nan, value=0, inplace = True)
	                
	                # -- Ratio desired is Coincidence - NonCoincidence (the average rate the MainFeature would have failed regardless of SubFeature failing)
	                CoincidenceCompare['DesiredRatio'] = CoincidenceCompare['CoincidenceRatio'] - CoincidenceCompare['NonCoincidenceRatio']
	                
	                # -- Archive Ratios and Counts for this particular category
	                CategoryRatios[MainFeature +'|'+ SubFeature] = CoincidenceCompare['DesiredRatio']
	                CategoryCounts[MainFeature +'|'+ SubFeature] = CoincidenceCompare['OccuranceCount']
	    
	    # -- Need weighted average for zip codes.  Weights are the counts of occurances over total number of 
	    Weights = CategoryCounts.div(CategoryCounts.sum(axis=1), axis=0)  

	    # -- Mask null values of Ratios so that average across axis can be computed
	    MaskedCategoryRatios = np.ma.MaskedArray(CategoryRatios, mask=np.isnan(CategoryRatios))

	    # -- Compute Average across Axes          
	    CategoryRatios['AverageRatio'] = np.ma.average(MaskedCategoryRatios, axis=1, weights=Weights)
	    CoincidenceRatios[CategoryName] = CategoryRatios['AverageRatio']

	CoincidenceRatios.to_csv(outputFile, sep=',')


if __name__ == "__main__":
	# running with 'python fileName inputDataFrame outputPath SpatialKey'
	if len(sys.argv) == 4:
		InputFile = sys.argv[1]
		OutputPath = sys.argv[2]
		SpatialKey = sys.argv[3]

		data = pd.DataFrame.from_csv(InputFile, sep='\t')
		
		# -- Clean data
		data['NYC'] = 'NYC'
		Replace3With1(data)
		ReplaceBoroughs(data)

		if SpatialKey in data.columns:
			BuildRatios(data, OutputPath + 'CoincidenceRatios_By_%s.csv' % (SpatialKey))
		else:
			print '\nError: %s not found as valid attribute of %s' % (SpatialKey, sys.argv[1])
		
	else:
		print '\nError: Usage is: python %s <input_file> <output_path> <key_used_against_spatial_query>' % (sys.argv[0])
		print 'Example: python %s myDataFrame.csv myOutputpath ZIPCODE' % (sys.argv[0])
else:
	print 'Imported: ' + sys.argv[0]

