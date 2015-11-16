import os
import sys
from datetime import datetime
from MasterDataframe import Read_Dataframe
import pandas as pd
import ScoreMetric
import ExternalData

# -- Output Path
out_path = 'Output'

def Build_Output_Paths(years, UseFiscal, spatialKey):

    if UseFiscal:
        YearType = 'FiscalYr'
    else:
        YearType = 'CalendarYr'

    nonSpatial_path = os.path.join(out_path,
                                   datetime.now().strftime('%m-%d-%Y'),
                                   years.replace(',','&'),
                                   YearType)
    
    spatial_path = os.path.join(nonSpatial_path, spatialKey)
    regression_path = os.path.join(spatial_path, 'Regressions')

    # -- Full Path assures all subpaths are built
    if not os.path.exists(spatial_path):
        os.makedirs(spatial_path)

    return (nonSpatial_path, spatial_path, regression_path)


if __name__ == '__main__':
    
    externalDataSpatialKeys = ['ZIPCODE', 'GEOID']
    metricPrompts =   {1: 'NaiveMetric',
                       2: 'AreaWeightedMetric',
                       3: 'AreaAmenityWeightedMetric'}
    spatialPrompts =  {1:'ZIPCODE',
                       2:'GEOID',
                       3:'Boro',
                       4:'District'}
    calendarPrompts = {1:True, 2:False}
    UseFiscal = False
    prompt = '> '

    
    # -- User input of spatial granularity
    print('\nWhat spatial key would you like to build against?')
    print('\t1: Zipcode\n\t2: Census Tract\n\t3: Boro\n\t4: District')
    print('Enter [1,2,3,4]')
    spatialKey = spatialPrompts[int(raw_input(prompt))]

    
    # -- User input of time period
    print('\nWhat Year or Years would you like to build against?'
          '  [ie. All, 2004 or 2004,2005,2006]')
    years = raw_input(prompt).split(',')

    try:
        years = [int(year) for year in years]
    except:
        # Defaults to All years and maintains case-insensitivity for
        # directory path
        years = ['All']

    if 'All' not in years:
        # Trick using Dicts.  Prompt enter of 1 converts to True.  2
        # converts to False
        print('\nWhat date range would you like to use?')
        print('\t1: Fiscal Year\n\t2: Calendar Year')
        print('Enter [1,2]')
        UseFiscal = calendarPrompts[int(raw_input(prompt))]

        
    # -- Check for data
    if spatialKey not in externalDataSpatialKeys:
        print('\nPlease note: %s based external data sets do not exist.'
              '  Regressions are not being generated.' % (spatialKey))
#        print('  bailing out...')
#        sys.exit()


    # -- define regressions
    print('\nWhich score metric would you like regressions built from?')
    print('\t1: Basic Average\n\t2: Weighted by Area\n'
          '\t3: Weighted by Area and Amenities')
    print 'Enter [1,2,3]'
    metricToRegress = int(raw_input(prompt))


    # -- Read Dataframe
    if 'All' not in years:
        df = Read_Dataframe(UseFiscal, years)
    else:
        df = Read_Dataframe()


    # -- Naive Park Scores
    naiveParkScoresDf = ScoreMetric.Park_Naive_Scores(df)

    
    # -- Create Scores
    scoresDf = ScoreMetric.Create_Scores(df, spatialKey)

    
    # -- Build directory structure for outputs
    (nonSpatial_path, spatial_path, regression_path) = \
        Build_Output_Paths('&'.join(map(str, years)), UseFiscal, spatialKey)

    
    # -- Write Scores
    naiveParkScore_file = os.path.join(nonSpatial_path,
                                       'NaiveParkLevelScores.csv')
    score_file = os.path.join(spatial_path,
                              'SpatialAggregatedQualityScores.csv')

    naiveParkScoresDf.to_csv(naiveParkScore_file, sep=',', index=False)
    scoresDf.to_csv(score_file, sep=',', index=False)

    
    # -- Read External Data
    if spatialKey in externalDataSpatialKeys:
        
        # -- Build Directory
        regressionFull_path = os.path.join(regression_path,
                                           metricPrompts[metricToRegress])
        if not os.path.exists(regressionFull_path):
                os.makedirs(regressionFull_path)

        # -- Collect Data for Regression
        scoresToRegress = scoresDf.set_index(spatialKey) \
                                  .ix[:,metricToRegress-1]  
        externalDf = ExternalData.Read_External_Data(spatialKey) 

        if externalDf.empty is True:
            print('Warning:  No External Data at the requested spatial '
                  'granularity is available... ignoring regression analysis.')
        else:
            # Regress, Plot, and Save each regression using columns of
            # external data
            for feature in externalDf.columns:
                externalFeatureToRegress = externalDf.ix[:,feature]
                
                # Merge and clean
                regressDf = pd.concat([scoresToRegress,
                                       externalFeatureToRegress], axis=1)
                regressDf.dropna(inplace=True)
                regressDf = regressDf[regressDf[externalFeatureToRegress.name]
                                      != 0]
                scoresToRegressCleaned, externalFeatureToRegressCleaned = \
                        regressDf.ix[:,0], regressDf.ix[:,1]
                
                regressionPlot = ExternalData \
                        .Run_Regression(scoresToRegressCleaned,
                                        externalFeatureToRegressCleaned)
                plot_file = os.path.join(regressionFull_path,
                                         feature.replace(" ", "") + '.png')
                regressionPlot.savefig(plot_file)

                # -- Write Raw Data
                regressionRawFull_path = os.path.join(regressionFull_path,
                                                      'RawData')
                regressionRawFull_file = os.path.join(regressionRawFull_path,
                                                      feature.replace(" ", "")
                                                      + '_RawData.csv')
                if not os.path.exists(regressionRawFull_path):
                        os.makedirs(regressionRawFull_path)
                regressDf.to_csv(regressionRawFull_file, sep=',', index=True)


    print 'Completed!  Outputs sent to: %s' % (os.path.join(os.getcwd(),
                                                            spatial_path, ""))




