#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pandas as pd
import xmltodict
import os

## might want to upgrade path wrangling

def parseXML(path):
	'''transform DPR_property xml to csv'''
	with open(path, 'r') as xmlfile:
    xdict = xmltodict.parse(xmlfile)
    x = xdict[xdict.keys()[0]]['facility']
    df = pd.DataFrame(x)
    df.to_csv(path.replace('xml','csv'), encoding='utf8')
    print 'Saved as CSV to :%s' % path.replace('xml','csv')


def main():
	parseXML(sys.argv[1])

if __name__ == '__main__':
	main()
    
