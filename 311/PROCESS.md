PROCESS
=======
##I. 311 Calls general analysis
- TBDescribed <<<- check env_variables as I changed them couble of days ago

##II. Computing park area for park districts:

** Park Districts | computing **
- read two shp files (park boundaries and park districts boundaries)
- calculate area for each park
- use crs in foots for both  <<<- to check!
- use spatial join on park centroids, getting **park district id** for each park
- collect park area and number of parks for each district
- collect park id's as array for each district
- calculate percent of park area vs total area for each district

- save districts with new data  as csv and geojson (**data/park_Districts_computed.csv**, **data/park_Districts_computed.geojson**, for geojson had to drop array of park ID's)
- save parks with area and **park district id** attribute (**data/parks_computed.geojson**)

##III. Categories aalysis for each park district

** Park District | categories  **
- read parks shp
- calculate percentage of area for each category for NYC
- calculate percentage of area for each category for each district in NYC

##IV. 311 TimeSeries
** 311 complains | locating   **
- read parc calls
- group by park and year
- save timeseries for each park (**311park_time_series.csv**)
- save timeseries for each Borough (**311park_boro_series.csv**)
- TODO: save timeseries for each District when recognise by district
- draw plots

##V. 311 per District     
** 311 complains | locating   **

As in total only ~30% of park calls are geolocated, I started to work on parks ontology (about a half of park_names for calls didn't match any name in parks open data)

- open calls
- open parks_computed (with PDistrict column added)
- matched calls vs parks <- ~ 4000 have no direct match
- saved unrecognised names into **311_unrecoginsed_parks.csv**
- saved ontology (outer match) as **data/park_ontology.csv**
- quite a lot of parks can be matched by hand (OpenRefine) OR using **[fuzzywussy](https://github.com/seatgeek/fuzzywuzzy)** - this is next TODO

TODO: locate each call by district
TODO: total park complains per District
TODO: total park complains per District, normalised by park area
TODO: time series for each district, absolete and normalised

##VI. Geolocate calls
**Geolocate calls**
- check how many calls can be localised:
total
park calls:  66395
park calls with coordinates:  14976
coordinates:  9164700
coordinates2:  9164700
coordinates3:  9164700
Address:  7862844
Intersections:  1818875
Landmark:  7265

##GENERAL TODO

- 311 complains park name ontology
- POSTGRES/MONGO Database
- Recognize park district for each complain
- show total and timeline of complains for each district normalised by park area
- geolocate calls for parks
- functional area for each park <-- geolocation of calls (of ~6 mln calls)


- we have time series now, so we can do timeseries clustering, or compare time series per park to quality time (need accseries
- I can compare complainds distribution to quailty distribution per park (ks-test)