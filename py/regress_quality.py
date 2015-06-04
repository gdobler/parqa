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
    ff_mi = pd.merge(ffrac,ny_data[['ZIP','median_hh_income']],
                     left_on='ZIPCODE', right_on='ZIP') \
                     .groupby('ZIP').first()

    # -- plot it
    fig, ax = plt.subplots(figsize=[10,5])
    ax.plot(ff_mi['median_hh_income']*1e-3,ff_mi['Overall Condition'],'o')
    ax.grid(1)
    ax.set_xlabel('Median Income [1000s of $]')
    ax.set_ylabel('Fraction of Overall Condition Faliures')
    fig.canvas.draw()
