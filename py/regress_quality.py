import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gp
from failure_fraction import *

if __name__=='__main__':

    # -- get the failure fraction
    try:
        ffrac
    except:
        ffrac = failure_fraction(2012)

    # -- read in income data
    print("reading NYC geographic data...")
    ny_file = '/scratch/www/files/gdobler/nycep/data/nyc-zip-code-extend.json'
    ny_data = gp.GeoDataFrame.from_file(ny_file)


    # -- combine failure fraction and median income then group by
    #    zipcodes to eliminate repeated zips in the income data file
    print("merging failure fraction with median income data...")
    ff_mi = pd.merge(ffrac,ny_data[['ZIP','median_hh_income','salary',
                                    'mean_distance','num_employees']],
                     left_on='ZIPCODE', right_on='ZIP') \
                     .groupby('ZIP').first()


    # -- plot it
    clrs = plt.rcParams['axes.color_cycle']

    fig, ax = plt.subplots(2,2,figsize=[10.5,6.5])
    fig.subplots_adjust(0.07,0.075,0.95,0.95)
    ax[0,0].plot(ff_mi['median_hh_income']*1e-3,
                 (1.0-ff_mi['Overall Condition'])*100,'o',color=clrs[0])
    ax[0,0].grid(1)
    ax[0,0].set_xlabel('Median Income [1000s of dollars]')
    ax[0,0].set_ylabel('% Overall Acceptable')
    
    ax[0,1].plot(ff_mi['mean_distance'],
                 (1.0-ff_mi['Overall Condition'])*100,'o',color=clrs[1])
    ax[0,1].grid(1)
    ax[0,1].set_xlabel('Mean distance to nearest park [ft]')
    ax[0,1].set_ylabel('% Overall Acceptable')
    
    ax[1,0].plot(ff_mi['num_employees']*1e-3,
                 (1.0-ff_mi['Overall Condition'])*100,'o',color=clrs[2])
    ax[1,0].grid(1)
    ax[1,0].set_xlabel('Number of Employees [1000s]')
    ax[1,0].set_ylabel('% Overall Acceptable')
    
    ax[1,1].plot(ff_mi['salary'],
                 (1.0-ff_mi['Overall Condition'])*100,'o',color=clrs[4])
    ax[1,1].grid(1)
    ax[1,1].set_xlabel('Average salary [1000s of dollars]')
    ax[1,1].set_ylabel('% Overall Acceptable')

    fig.canvas.draw()
    fig.savefig('../Outputs/external_factors_scatter.png', clobber=True)
