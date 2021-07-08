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


# %%
important_channels = pd.read_excel('important_channel_ids.xlsx')
specific_channel_folder = 'credible_channels'

less_video_channel_names = ['Johns Hopkins University', 'Johns Hopkins Medicine', 'Imperial College London']
# %%
if not os.path.exists(specific_channel_folder):
    os.mkdir(specific_channel_folder)

for organization in important_channels['Organization']:
    if not os.path.exists(os.path.join(specific_channel_folder, organization)):
        os.mkdir(os.path.join(specific_channel_folder, organization))


# %%
## 0 instances of SARS as a keyword for these

# early_month_range = [to_yt_time(pd.to_datetime(date)) for date in ['Dec 01, 2019', 'Jan 31, 2020']]
# less_video_channels = important_channels[important_channels['Organization'].isin(less_video_channel_names)]

# for i, channel_row in less_video_channels.iterrows():
#     print('Starting organization: ' + str(channel_row['Organization']))
#     this_channel_data = pd.DataFrame()
#     pageToken = None
#     while True:
#         query = video_information_from_search('SARS', youtube, channelId=channel_row['YT Channel ID'], time_range = early_month_range, order='viewCount', max_results=50, pageToken = pageToken, regionCode='ca')
#         output_df = query[0]
#         search_response = query[1]
#         if type(search_response) != dict:
#             search_response = search_response[0]
        
#         if len(this_channel_data) == 0:
#             this_channel_data = output_df
#         else:
#             this_channel_data = pd.concat([this_channel_data, output_df])

#         if 'nextPageToken' in search_response.keys():
#             pageToken = search_response['nextPageToken']
#         else:
#             print('Done.')
#             break
    
#     this_channel_data.to_csv(specific_channel_folder +'/'+channel_row['Organization']+'/'+early_month_range[0][:10]+'__'+ early_month_range[1][:10] + '_SARS.csv')

# %%
all_month_range = [to_yt_time(pd.to_datetime(date)) for date in ['Dec 01, 2019', 'Aug 30, 2020']]
less_video_channels = important_channels[important_channels['Organization'].isin(less_video_channel_names)]

for i, channel_row in less_video_channels.iterrows():
    print('Starting organization: ' + str(channel_row['Organization']))
    this_channel_data = pd.DataFrame()
    pageToken = None
    while True:
        query = video_information_from_search(search_query, youtube, channelId=channel_row['YT Channel ID'], time_range = all_month_range, order='viewCount', max_results=50, pageToken = pageToken, regionCode='ca')
        output_df = query[0]
        search_response = query[1]
        if type(search_response) != dict:
            search_response = search_response[0]
        
        if len(this_channel_data) == 0:
            this_channel_data = output_df
        else:
            this_channel_data = pd.concat([this_channel_data, output_df])

        if 'nextPageToken' in search_response.keys():
            pageToken = search_response['nextPageToken']
        else:
            print('Done.')
            break
    
    this_channel_data.to_csv(specific_channel_folder +'/'+channel_row['Organization']+'/'+all_month_range[0][:10]+'__'+ all_month_range[1][:10] + '.csv')

# %% 

more_video_channels = important_channels[~important_channels['Organization'].isin(less_video_channel_names)]
monthly_overall_time_range = time_range_maker('Dec 01, 2019', 'Aug 30, 2020', step=28, end_behavior='full_length')

for time_range in monthly_overall_time_range:
    if pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1:
        sq = search_query + '|SARS'
    else:
        sq = search_query
    print(time_range)
    for i, channel_row in more_video_channels.iterrows():
        print('Starting organization: ' + str(channel_row['Organization']))
        this_channel_data = pd.DataFrame()
        pageToken = None
        while True:
            query = video_information_from_search(sq, youtube, channelId=channel_row['YT Channel ID'], time_range = time_range, order='viewCount', max_results=50, pageToken = pageToken, regionCode='ca')
            output_df = query[0]
            search_response = query[1]
            if type(search_response) != dict:
                search_response = search_response[0]
            
            if len(this_channel_data) == 0:
                this_channel_data = output_df
            else:
                this_channel_data = pd.concat([this_channel_data, output_df])

            if 'nextPageToken' in search_response.keys():
                pageToken = search_response['nextPageToken']
            else:
                print('Done.')
                break
        this_channel_data.to_csv(os.path.join(specific_channel_folder, channel_row['Organization'])+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '.csv')
# %%
