#!/usr/bin/env python
#-*- coding: utf-8 -*-

# GEOCODER

from geopy.geocoders import GoogleV3 #GeocoderDotUS #GoogleV3 #Nominatim
geolocator = GoogleV3()


def geocodeDF(df, adress, add=', NYC'):
    '''geolocate data'''

    def geocode(x, geolocator):
	    '''geocode query'''
	    location = geolocator.geocode(x)
	    
	    if location:
	        return (location.latitude, location.longitude)
	    else:
	        print 'failed to find:',x
	        return (None,None)

    df['geo'] = df[adress].apply(lambda x: geocode(x+add, geolocator))
    df['lat'] = df['geo'].apply(lambda x:x[0])
    df['lon'] = df['geo'].apply(lambda x:x[1])
    df = df.drop(['geo'],axis=1)
    return df

# df = geocodeDF(df,'ADDRESS')
if __name__ == '__main__':
	pass