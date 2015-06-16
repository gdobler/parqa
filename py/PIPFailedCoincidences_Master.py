import pandas as pd
import numpy as np
import sys

Categories = { \
	'Cleanliness': [u'Glass', u'Graffiti', u'Ice', u'Litter', u'Weeds'], \
	'Structural' : [u'Benches', u'Fences', u'Paved Surfaces', u'Play Equipment', u'Safety Surface', u'Sidewalks'], \
	'Landscape' : [u'Athletic Fields', u'Horticultural Areas', u'Trails', u'Lawns', u'Trees', u'Water Bodies']}


def NonCoincidenceFailure(Data, Spatial, MainFeature, SubFeature):
    
    MainInspected = Data[MainFeature].notnull()
    SubInspected = Data[SubFeature].notnull()
        
    DataSub = Data[MainInspected & SubInspected][[Spatial, MainFeature, SubFeature]]
    DataSubGroup = DataSub.groupby(Spatial)
    
    Count = DataSubGroup.count()[MainFeature]
    Failures = DataSubGroup.sum()[MainFeature]
    NonCoincidenceRatio = 1 - Failures.astype(float) / Count
    
    DataReturn = DataSubGroup.first().reset_index()[[Spatial]].set_index(Spatial)
    DataReturn['NonCoincidenceRatio'] = NonCoincidenceRatio
    DataReturn['OccuranceCount'] = Count

    return DataReturn


def CoincidenceFailure(Data, Spatial, MainFeature, SubFeature):
   
    MainInspected = Data[MainFeature].notnull()
    SubInspected = Data[SubFeature].notnull()
    MainFailed = Data[MainFeature] == 0
    
    DataSub = Data[MainInspected & SubInspected & MainFailed][[Spatial, MainFeature, SubFeature]]
    DataSubGroup = DataSub.groupby(Spatial)
    
    Count = DataSubGroup.count()[MainFeature]
    Failures = DataSubGroup.sum()[SubFeature]
    CoincidenceRatio = 1 - Failures.astype(float) / Count
    
    DataReturn = DataSubGroup.first().reset_index()[[Spatial]].set_index(Spatial)
    DataReturn['CoincidenceRatio'] = CoincidenceRatio
    
    
    return DataReturn


def BuildRatios(df, outputFile):

	# -- Create DataFrame with ZIPCODE as index
	CoincidenceRatios = df.groupby(SpatialKey).first().reset_index()[[SpatialKey]].set_index(SpatialKey)

	# -- For each Category, build seperate Ratio and Counts of all feature comparisons
	for CategoryName, CategoryValues in Categories.iteritems():

	    CategoryRatios = df.groupby(SpatialKey).first().reset_index()[[SpatialKey]].set_index(SpatialKey)
	    CategoryCounts = df.groupby(SpatialKey).first().reset_index()[[SpatialKey]].set_index(SpatialKey)

	    # -- For each MainFeature, compare it to all SubFeatures as long as they are not the same
	    for MainFeature in CategoryValues:
	        for SubFeature in CategoryValues:
	            if MainFeature is not SubFeature:
	               
	                # -- Call for Coincidence Ratio and NonCoincidence Ratios to be built and merged, indexed by Zip
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
	# running with 'python fileName inputDataFrame outputFileName'
	if len(sys.argv) == 4:
		data = pd.DataFrame.from_csv(sys.argv[1], sep='\t')
		SpatialKey = sys.argv[3]
		if SpatialKey in data.columns:
			BuildRatios(data, sys.argv[2])
		else:
			print '\nError: %s not found as valid attribute of %s' % (SpatialKey, sys.argv[1])
		
	else:
		print '\nError: Usage is: python %s <input_file> <output_file> <key_used_against_spatial_query>' % (sys.argv[0])
		print 'Example: python %s myDataFrame.csv myOutputFile.csv ZIPCODE' % (sys.argv[0])
else:
	print 'Imported: ' + sys.argv[0]

