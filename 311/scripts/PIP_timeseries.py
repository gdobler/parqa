import os
import sys
from datetime import datetime
from MasterDataframe import Read_Dataframe
import pandas as pd
import ScoreMetric
import ExternalData


## for now hardcoded 2004-2015 range. should change that


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

    
    print('\nWhat date range would you like to use?')
    print('\t1: Fiscal Year\n\t2: Calendar Year')
    print('Enter [1,2]')
    UseFiscal = calendarPrompts[int(raw_input(prompt))]

        
    # -- Check for data
    if spatialKey not in externalDataSpatialKeys:
        print('\nPlease note: %s based external data sets do not exist.'
              '  Regressions are not being generated.' % (spatialKey))
        # print('  bailing out...')
        # sys.exit()


    # -- define regressions
    print('\nWhich score metric would you like regressions built from?')
    print('\t1: Basic Average\n\t2: Weighted by Area\n'
          '\t3: Weighted by Area and Amenities')
    print 'Enter [1,2,3]'
    metricToRegress = int(raw_input(prompt))


    
    # -- TIMESERIES - for now only spatial
    scores_tmp = []
    for year in xrange(2004,2016):
        print 'processing... ', year
        df = Read_Dataframe(UseFiscal, [year])
        df['District'] = df['Boro'] + '-' +df['District']

        # -- Naive Park Scores - dont need them for now
        # naiveParkScoresDf = ScoreMetric.Park_Naive_Scores(df)
            
        # -- Create Scores
        s = ScoreMetric.Create_Scores(df, spatialKey).set_index(spatialKey)
        s = s.stack().reset_index().rename(columns={0:int(year),'level_1':'score_type'})
        scores_tmp.append(s)

    # -- create single dataframe
    result = scores_tmp[0]
    for temp_df in scores_tmp[1:]:
        result = result.merge(by=['score_type','District'], how='outer')


    path = os.getenv('PWD') + '/PIP_score_timeseries.csv'
    result.to_csv(path)




    print 'Completed!  Outputs sent to: %s' % path




