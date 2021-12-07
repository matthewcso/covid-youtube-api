# %%
from master_controller import *
from ytsearch import *
import pandas as pd
import os
from googleapiclient.discovery import build
from datetime import datetime

from devkeys import devkeys

output_dir = 'updated_yt_data'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

search_query = 'coronavirus|covid|wuhan'
i=0

overall_time_range = time_range_maker('Aug 01, 2021', datetime.now() - pd.Timedelta(7, 'days'))

for week_n, time_range in enumerate(overall_time_range):
    # Switch developer key due to usage limitations - not a problem in Aug 2020 but would be a problem for future
    if week_n % 45 == 0: 
        DEVELOPER_KEY = devkeys[i]
        youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)
        i += 1

    print(time_range)

    if (pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1) and (pd.to_datetime(time_range[0]).year < 2021):
        sq = search_query + '|SARS'
    output_df, request_info = video_information_from_search(sq, youtube, time_range=time_range, regionCode='ca')
    output_df.to_csv(output_dir+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '.csv')


# %%
