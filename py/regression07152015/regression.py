import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import DataFrame as df
import os


def generate_plot_folder(all_files_in_external_data, all_years_in_table, l):
    features = ['PopulationDensity',
                'AreaLand',
                'TotalPopulation',
                'Median Age',
                'MinorityPercentage',
                'PercentageUnemoployment',
                'MedianhouseholdIncome',
                'HouseholdsGiniIndex',
                'Market_Val',
                'TotalMidMarchEmployees',
                'TotalAnnualPayroll($1,000)',
                'TotalNumberofEstablishments']
    # 'TotalPopulationPerFunctionArea',
    # 'WorkersPerFunctionArea']
    x = df.from_csv(all_files_in_external_data)
    y = df.from_csv(all_years_in_table)
    if all_years_in_table.split('_')[1] == 'ZIPCODE':
        newtable = y.merge(x, how='left', left_on='ZIPCODE', right_on='ZipCode')
    else:
        newtable = y.merge(x, how='left', on='CENSUSTRACT')
    for i in features:
        x = sm.add_constant(newtable[i])
        y = newtable[l]
        res = sm.OLS(y, x).fit()
        R2 = res.rsquared
        plt.scatter(x[i], y, color='blue')
        plt.plot(x[i], res.fittedvalues, color='red', linewidth=4)
        plt.ylabel(l)
        plt.xlabel(i + '<R^2 = ' + str(R2) + '>')
        plt.title(l + ' vs ' + i + ' '.join(all_years_in_table.split('_')[1:4]))
        if not os.path.exists('_'.join(all_years_in_table.split('_')[1:4])):
            os.makedirs('_'.join(all_years_in_table.split('_')[1:4]))
        plt.savefig(
            '_'.join(all_years_in_table.split('_')[1:4]) + '/' + l + '_vs_' + i + '_'.join(all_years_in_table.split('_')[1:4]))
        plt.clf()

if __name__ == '__main__':

    ###########################################################################
    ############################   Demo        #########################
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
                for l in socres:
                    all_files_in_external_data = path_to_data_summary +\
                        j + Data_Summary
                    all_years_in_table = path_to_quality_score +\
                        '_'.join(['ParkQuality', j, str(i), k]) + '.csv'
                    print all_files_in_external_data, all_years_in_table
                    generate_plot_folder(
                        all_files_in_external_data, all_years_in_table, l)
    ###########################################################################
    ###########################################################################
