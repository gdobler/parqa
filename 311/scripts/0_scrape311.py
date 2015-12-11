#!/usr/bin/env python
#-*- coding: utf-8 -*-

# retrieve 311 calls open data from
# NYC open data
# https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9

# Philipp Kats, pbk236@nyu.edu
# october 2015

# script requires PARQA alias

# import pandas as pd
# import urllib
import requests
import datetime
import urllib


def getCalls(start=datetime.datetime(2010,1,31), end=datetime.datetime(2010,2,1)):
	'''retrieve calls data from
	NYC open data portal via socrata soda api and filtering by date range.
	check dataset here: 
	https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9'''
	
	ID = 'erm2-nwe9'
	timeQuery = "where=created_date between '%s' and '%s'" % (start.strftime('%Y-%m-%d'), 
													  end.strftime('%Y-%m-%d'))
	            
	SodaPath = "https://nycopendata.socrata.com/api/views/%s/rows.json?accessType=DOWNLOAD&%s" % (ID, urllib.quote(timeQuery))
	print SodaPath
	
	
	jd = requests.get(SodaPath) #.json()
	print jd.status()
	# print jd
	# return jd

def main():
	data = getCalls()


if __name__ == '__main__':
	main()

	