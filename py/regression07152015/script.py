from regression import generate_plot_folder
scores = ['Naive Normalized Score', 'Area Normalized Score',
          'Amenities & Area Normalized Score']
path_to_data_summary = '../externalData/'
Data_Summary = 'ExternalDataSummary.csv'

path_to_quality_score = '../Table/ParkQualityScores/'
years = [2010, 2011, 2012, 2013, 2014, 2015]
spatial_level = ['ZIPCODE', 'CENSUSTRACT']
time_format = ['FiscalYr', 'CalendarYr']
Quality_Score = []
for i in years:
    for j in spatial_level:
        for k in time_format:
            for l in scores:
                all_files_in_external_data = path_to_data_summary +\
                    j + Data_Summary
                all_years_in_table = path_to_quality_score + \
                    '_'.join(['ParkQuality', j, str(i), k]) + '.csv'
                print all_files_in_external_data, all_years_in_table
                generate_plot_folder(
                    all_files_in_external_data, all_years_in_table, l)
