# covid-youtube-api
My code from the COVID YouTube Analytics project at Mac-Theobio.
This is a utilization of the YouTube API v3 to get COVID-related data. 

This project proposes to analyze misinformation and trends in views on COVID through looking at the content of YouTube videos. 
It also seeks to compare differences between popular common videos and videos from public health sources such as the WHO. 

More details will be described as the project progresses. 

Videos that were taken down between the running of the first run and the update run are coded as having negative values in view, comment, etc. counts.
The updater.py performs updates comment, view, etc. counts in-place, as there are some human-derived metrics that can't be easily re-derived on a whim. 
If you don't care about this use-case, just rerun the initial_downloader.py.

Each time range includes the first date (e.x. October 9) at 12:00:01 AM, and the second date (e.x. October 16) at 12:00:00 AM.
