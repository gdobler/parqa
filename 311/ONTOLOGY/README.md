LOCATING 311 CALLS
==================

All in this folder works for one simple task: to match 311 calls
to related parks or other DPR property. As Calls database have "Park Facility Name" column, it seems quite an easy task,
though it is not. Half of the names are either fuzzy, unoficcial, outdated, or, sometimes, totally unrecognizable. To solve this task, following actions were made:

- [X] All 311 calls from NYC Open Data portal were collected
- [X] They were joined into one dataframe, and filtered by **Agency == DPR** and **Location not in (Streers, Streets/Curbs) ** (as we are interested in DPR proprty only).   This resulted in ... calls from 2010 til now  (TBD)
- [X] All **Facility Name** values vere deduped, unique values were saved as a left part of ontlogy (ontology in this case is marely key:value table)
- [X] On the other hand, park properties datasets were collected. Due to specifics of 311 calls, I had to collect all different types of properties frop open sources, such as **recreation centers, school playgrounds, golf courses, playgrounds, parks, beaches, pools** (links to be defined). 
- [X] Each dataset was parsed (most of them available as XML, few (recreation centers and golf courses) were geocoded using google API and checked manually. 
- [X] Again, each dataset was spatially joined (using their centroids) with Park District boundaries. [Notebooks](wrangling_DPR/dpr_add_parkDistrict/)
- [X] Then, list of unique 311 locations (left part of ontology) was checked against names in datasets in several steps [Notebook](Ontology2.0.ipynb):
	- 100% matching agains parks
	- impirical matching (dictionary, defined in process, helps to solve most popular ones, for example, all calls with "central park" in location automatically match "central park" location)
	- all names with "pool" in the location are matched against pools dataset (here and below I start using FUZZYWUZZY module for fuzzy matching. Module helps to find a best candidate from list provided)
	- all names with "recreation" in the location were matched against recreation centers dataset
	- all names with "beach" in the location were matched against beaches dataset
	- all names with "golf" in the location were matched against golf courses dataset
	- all names with "playground" in the location were matched against playgrounds dataset
	- all names with "ps" in the location were matched against school playgrounds dataset
	- all other names were matched against parks dataset
	here sequense was defined imirically and matters, as a lot of properties have overlapping names. This approach helped to recognize with 100% accuracy about 85% of calls. As a result, right part of the ontolgy was formed, including "correct" name, dataset (parks or pools, for example), and matching ratio (from 0 to 100%).
- [X] All ontology then was checked manually (using Open Refine). during the check, almost 100% of the dataset was recognized (apart of few unrecognizable names). Also, code (Ontology) was updated to improve it perfomance for future usage.
- [x] All data (mainly,geolocation and Park District ID) was added to ontology (right side). Several missing pD IDs (mainly for riverside parks) were handled manually
- [X] Using ontology, each call was matched to specific DPR property and therefore park district and geolocation.



