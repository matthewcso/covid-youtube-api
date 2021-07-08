# %%
from master_controller import *
from ytsearch import *
import json
import csv
import pandas as pd
import os
import threading
import isodate
from googleapiclient.discovery import build
from datetime import datetime

#for time_range in overall_time_range[:10]:
#    if pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1:
#        sq = search_query + '|SARS'
#    print(time_range)
#    output_df, request_info = video_information_from_search(sq, youtube, time_range=time_range)
#    print(output_df)

# %%
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.exists(n_post_dir):
    os.mkdir(n_post_dir)

for time_range in overall_time_range:
    print(time_range)
    if pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1:
        sq = search_query + '|SARS'
    output_df, request_info = video_information_from_search(sq, youtube, time_range=time_range, regionCode='KR')
    output_df.to_csv(output_dir+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '.csv')
