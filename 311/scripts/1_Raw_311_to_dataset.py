#!/usr/bin/env python
#-*- coding: utf-8 -*-

# refine 311 chunks of data, returning single 
# .csv file with calls related only to DPR agency
# and only DPR property (not streets)
# Philipp Kats, pbk236@nyu.edu
# october 2015

# script requires PARQA alias


import pandas as pd
import os
import sys


def getAllFiles(path, frmt=None, full=False):
    '''return all files in the folder,
    filtered by format, if it was provided'''
    
    fs = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if frmt!=None:
            fsTmp = [fl for fl in filenames if fl.endswith(frmt)]
            fs.extend(fsTmp)
        else:
            fsTmp = filenames
            fs.extend(fsTmp)
    if full:
        return [path+f for f in fs]
    else:
        return fs

def filterDPR(df):
    '''returns calls for DPR and not related to streets'''
    return df[(df.Agency == 'DPR')& (~df['Location Type'].isin(['Street/Curbside','Street']))]
   
def main():    
    PARQA= os.getenv('PARQA')

    dataPath = PARQA + 'data/RAW/raw_download/'
    df = pd.concat((pd.read_csv(x) for x in getAllFiles(dataPath,'.csv', full=True))).drop_duplicates()
    print 'General dataset consist of {1} rows'.format(len(df))    
    print '''Now I am filtering rows, keeping only ones related to DPR
    and not located on streets'''

    result = filterDPR(df)
    print "It's about {:1f}% of total 311 dataset".format(100.0*len(result)/len(df)) 
    print
    print result['Location Type'].value_counts()


    if len(sys.argv)>1:
        rPath = sys.argv[1] 
        if not p.endswith('.csv'):
            rPath+='311DPR1.csv'
    else:
        rPath = PARQA + '/data/311DPR.csv'

    result.to_csv(rPath, encoding='utf8')


if __name__ == '__main__':
    main()


