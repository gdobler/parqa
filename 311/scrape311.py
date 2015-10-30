# created_date

import pandas as pd
import urllib
import requests
import datetime


def getCalls(start=datetime.datetime(2009,12,31), end=datetime.datetime(2010,1,2)):
	'''retrieve calls data from
	NYC open data portal via socrata soda api and filtering by date range.
	check dataset here: 
	https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9'''
	ID = 'erm2-nwe9'
	timeQuery = "where=created_date between '%s' and '%s'" % (start.strftime('%Y-%m-%d %H:%M:%S'), 
													  end.strftime('%Y-%m-%d %H:%M:%S'))

	SodaPath = "https://nycopendata.socrata.com/api/views/%s/rows.json?accessType=DOWNLOAD&%s" % (ID, timeQuery)
	# print SodaPath
	
	jd = requests.get(SodaPath).json()
	# df = pd.read_csv(urllib.quote(SodaPath))
	# print df.columns
	# print len(df)
	return jd

print 'hey'
print getCalls()
print 'yey'
	