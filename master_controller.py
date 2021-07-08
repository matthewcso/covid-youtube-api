# TODO: Fix rare bug where if a video becomes unavailable between search and statistics getting, the program will not work.

# %%
from ytsearch import *
import json
import csv
import pandas as pd
import os
import threading
import isodate
from googleapiclient.discovery import build
from datetime import datetime

DEVELOPER_KEY = "AIzaSyCyNg_ahXZj5oaePErxCEp_3S2u2xsCGPw"
search_query = 'coronavirus|covid|wuhan'

overall_time_range = time_range_maker('Dec 01, 2019', 'Aug 30, 2020')#datetime.now())

output_dir = 'updated_yt_data_kr2'
n_post_dir = 'n_posts'
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

def video_information_from_search(search_query, youtube, time_range=[-1, -1], pageToken = None, order='viewCount', regionCode='ca', channelId=None, max_results=30):

    search = youtube_search(search_query, youtube, order=order, max_results=max_results, time_range=time_range, pageToken = pageToken, regionCode=regionCode, channelId=channelId)
    output_df = pd.DataFrame()
    search_response,searched_channelId,videoId,title,publishedAt = search

    if time_range != [-1, -1]:
        output_df['codingWeek'] = [time_range[0][:10]+'-'+ time_range[1][:10] for _ in range(len(searched_channelId))]
    output_df['channelId'] = searched_channelId
    output_df['videoId'] = videoId
    output_df['title'] = title
    output_df['publishedAt'] = publishedAt

    print('Finished Query. ')

    print('Total number of results: ' + str(len(output_df['videoId'])))

    if len(output_df['videoId']) == 0: # break if no videos found
        return output_df, search_response
    video_stats = youtube_videos(output_df['videoId'].tolist(), youtube)

    output_df['viewCount'] = video_stats[1]
    output_df['likeCount'] = video_stats[2]
    output_df['dislikeCount'] = video_stats[3]
    output_df['commentCount'] = video_stats[4]
    output_df['favoriteCount'] = video_stats[5]
    output_df['duration'] = video_stats[6]

    channel_stats = youtube_channels(output_df['channelId'].tolist(), youtube)
    output_df['channelTitle'] = channel_stats[1]
    output_df['subscriberCount'] = channel_stats[2]
    output_df['country'] = channel_stats[3]

    output_df['videoURL'] = ['https://www.youtube.com/watch?v='+i for i in output_df['videoId']]
    output_df['duration'] = [isodate.parse_duration(i).seconds for i in output_df['duration']]
    
    output_df = output_df.drop(columns=['favoriteCount'])

    if channelId is not None:
        output_df = output_df[output_df['channelId'].str.contains(channelId)]
    print()
    return output_df, search
