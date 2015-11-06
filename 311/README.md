PARQA 311
=========


## Phases

- [x] Collecting 311 calls from [open source](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9)
- [x] Filtering 311 calls, keeping only DPR property related calls (Agency=DPR)(Location!=Streets/Curbs) [Notebook](1_Raw_311_to_dataset.ipunb), [Script](scripts/1_Raw_311_to_dataset.py)
- [x] Creating ontology to match calls to facilities. [INFO](ONTOLOGY/README.md)
- [x] Calls matching to facilities and park districts [Notebook](4_Matching_Calls_Districts.ipynb)
- [x] Create time series of calls for each park district. [Notebook](5_Calls_Timeseries.ipynb)
- [ ] time series of park quality for each park district. [Notebook](3_PIP_timeseries.ipynb)
- [ ] correlation between time series
- [ ] tables of complain type for each district and/or park.


## Sources
- [List of used and potential sources](PARKS_OPEN_DATA.md)
