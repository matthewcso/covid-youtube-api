# %%
from master_controller import *
from ytsearch import *
import pandas as pd
import os
from googleapiclient.discovery import build
from datetime import datetime

# IMPORTANT: you need to create a devkeys.py and put in a Python list of YouTube API developer keys.
# Instructions for doing this can be found here: https://developers.google.com/youtube/v3/getting-started
from devkeys import devkeys

output_dir = 'updated_yt_data'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

search_query = 'coronavirus|covid|wuhan'
i=0

overall_time_range = time_range_maker('Dec 29, 2019', datetime.now() - pd.Timedelta(7, 'days'))


DEVELOPER_KEY = devkeys[i]
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
i += 1

for week_n, time_range in enumerate(overall_time_range):
    def run():
        print(time_range)
        if (pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1) and (pd.to_datetime(time_range[0]).year < 2021):
            sq = search_query + '|SARS'
        else:
            sq = search_query
        output_df, request_info = video_information_from_search(sq, youtube, time_range=time_range, regionCode='ca', max_results=30)
        output_df.to_csv(output_dir+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '.csv')

    try:    # Switch developer key due to usage limitations - not a problem in Aug 2020 but would be a problem for future
        run()

    except HttpError:
        DEVELOPER_KEY = devkeys[i]
        youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)
        i += 1
        run()

# %%
