#!/usr/bin/env python
#-*- coding: utf-8 -*-

# collect time series per district for PIP quality scores 
# from path of output data

# Philipp Kats, pbk236@nyu.edu
# october 2015

# script requires PARQA alias

import pandas as pd
import os

PARQA = os.getenv('PARQA')


def getAllFiles(path, frmt=None, full=False):
    '''return all files in the folder,
    filtered by format, if it was provided'''

    fs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if frmt!=None:
            fsTmp = [dirpath + '/' + fl for fl in filenames if fl.endswith(frmt)]
            fs.extend(fsTmp)
        else:
            fsTmp = filenames
            fs.extend(fsTmp)
    if full:
        return [path+f for f in fs]
    else:
        return fs


def main():
    path = PARQA + 'data/PIP_TIMESERIES/11-01-2015'

    # path to all files
    scores = [x for x in getAllFiles(path,'.csv', False) if 'SpatialAggregated' in x]

    df = pd.DataFrame({score.split('/')[-4]:pd.read_csv(score, index_col='District')['Amenities & Area Normalized Score'] for score in scores})
    df.to_csv(PARQA + 'data/PIP_Districts_timeseries.csv')

if __name__ == '__main__':
    main()

