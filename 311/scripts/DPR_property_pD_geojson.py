#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pandas as pd
import geopandas as gp
import os

from shapely.geometry import Point
from geopandas.tools import sjoin

PARQA = os.getenv('PARQA')


def toGeoDataFrame(df, lat='lat',lon='lon'):
    '''dataframe to geodataframe'''
    df = df[pd.notnull(df[lat])]

    df['geometry'] = df.apply(lambda z: Point(z[lon], z[lat]), axis=1)
    df = gp.GeoDataFrame(df)
    df.crs = {'init': 'epsg:4326', 'no_defs': True}
    return df 


def writeGeoJson(gdf,path):
	'''writes df as json'''
	with open(path,'w') as jsFile:
		jsFile.write(gdf.to_json())


def everything(path):
	''''''
	pD = gp.read_file(PARQA + 'data/SHP/Park_Districts/ParkDistrict.shp')[['SYSTEM','geometry']]
	df = toGeoDataFrame(pd.read_csv(oath, index_col=0))

	df = df.to_crs(pDistricts.crs)
	df = sjoin(df, pD, how="left").rename(columns={'SYSTEM':'parkDistrict'})
	df = df.to_crs(epsg=4326)

	rPath = path.replace('.csv','.json')
	writeGeoJson(df, rPath)




def main():
	everything(sys.argv[1])
	pass

if __name__ == '__main__':
	main()