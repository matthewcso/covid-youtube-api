import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
import csv
from unidecode import unidecode
import pandas as pd
import numpy as np
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#search for videos



def youtube_search(q, youtube, max_results=30 ,order="viewCount", time_range = [-1, -1], pageToken = None, regionCode='ca', channelId = None):

    if pageToken is not None:
        assert time_range != [-1, -1]
        search_response = youtube.search().list(
            part="snippet",
            eventType="none", 
            maxResults= max_results, 
            order=order, 
            q=q, 
            publishedAfter=time_range[0],
            publishedBefore=time_range[1],
            type="video", 
            videoType="any",
            pageToken = pageToken,
            regionCode = regionCode,
            channelId=channelId,
            relevanceLanguage = "en"
            ).execute() 
    elif time_range == [-1, -1]:
        search_response = youtube.search().list(
            part="snippet",
            eventType="none", 
            maxResults= max_results, 
            order= order, 
            q=q, 
            type="video", 
            videoType="any",
            regionCode=regionCode,#'ca',
            channelId=channelId,
            relevanceLanguage = "en"
            ).execute() 
    else:
        search_response = youtube.search().list(
            part="snippet",
            eventType="none", 
            maxResults= max_results, 
            order= order, 
            q=q, 
            publishedAfter=time_range[0],
            publishedBefore=time_range[1],
            type="video", 
            videoType="any",
            regionCode=regionCode, #'ca',
            channelId=channelId,
            relevanceLanguage = "en"
            ).execute() 

    channelIds = []
    videoIds = []
    titles = []
    publishedAts = []
    kinds = []

    for search_result in search_response.get("items", []):
      channelIds.append(search_result["snippet"]["channelId"])
      videoIds.append(search_result["id"]["videoId"])
      title = search_result["snippet"]["title"]
      title = unidecode(title)
      titles.append(title)
      publishedAts.append(search_result["snippet"]["publishedAt"])

    return(search_response,channelIds,videoIds,titles,publishedAts)


#get stats of each video
#use videoId of each video from search_response
def youtube_videos(videoIds, youtube):
    video_response = youtube.videos().list(
        id=videoIds,
        part="statistics,contentDetails"
        ).execute()

    ids = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    duration = []
    for video_result in video_response.get("items",[]):
        if 'viewCount' not in video_result["statistics"]:
              viewCount.append(np.nan)
        else:
              viewCount.append(video_result["statistics"]["viewCount"])
        if 'likeCount' not in video_result["statistics"]:
              likeCount.append("N/A")
        else:
              likeCount.append(video_result["statistics"]["likeCount"])
        if 'dislikeCount' not in video_result["statistics"]:
              dislikeCount.append("N/A")
        else:
              dislikeCount.append(video_result["statistics"]["dislikeCount"])
        if 'commentCount' not in video_result["statistics"]:
              commentCount.append("N/A")
        else:
              commentCount.append(video_result["statistics"]["commentCount"])
        if 'favoriteCount' not in video_result["statistics"]:
              favoriteCount.append("N/A")
        else:
              favoriteCount.append(video_result["statistics"]["favoriteCount"])
        if 'duration' not in video_result["contentDetails"]:
              duration.append("N/A")
        else:
              duration.append(video_result["contentDetails"]["duration"])
        ids.append(video_result['id'])

        #ids.append(video_result[''])
        
    return(video_response,viewCount,likeCount,dislikeCount,commentCount,favoriteCount, duration, ids)


#get channel name and sub count
#use channelId of each video from search_response
def youtube_channels(channelIds, youtube):
    channel_response = youtube.channels().list(
        id = channelIds,
        part = "snippet,statistics,id,brandingSettings"
        ).execute()

    lookup = {}
    
    for channel_result in channel_response.get("items", []):
        if "country" in channel_result["brandingSettings"]["channel"].keys():
            channel_country = channel_result["brandingSettings"]["channel"]['country']
        else:
            channel_country = "Unknown"
        if 'subscriberCount' in channel_result['statistics'].keys():
            subs = channel_result['statistics']['subscriberCount']
        else:
            subs = np.nan
        lookup[channel_result['id']] = (channel_result["snippet"]["title"],subs ,channel_country)
    titles = []
    subscriberCount = []
    country = []
    for channel in channelIds:
        titles.append(lookup[channel][0])
        subscriberCount.append(lookup[channel][1])
        country.append(lookup[channel][2])

    return channel_response, titles, subscriberCount, country
 


# %%
def to_yt_time(time):
    """
    Converts pandas timestamps into Google strings. Not the most robust implementation, but it works
    Args:
        time (pd.Timestamp)
    Returns:
        str
    """
    return str(time)[:10] +'T' + str(time)[11:19]+'Z'

def time_range_maker(start_time, end_time, step=7, end_behavior='clip'):
    """
    Creates a series of beginning and end datetimes for (default) weekly intervals between start_time and end_time.
    Args:
        start_time, end_time (str or datetime-like)
        step (int): number of days in an interval
        end_behavior: 'clip': If your last week has less than 7 days in it, remove it.   
                    'full_length': If your last week has less than 7 days in it, return results coming before end_time.
    Returns:
        list([str, str])
    """
    current_time = pd.to_datetime(start_time)
    pd_end_time = pd.to_datetime(end_time)
    step_timedelta = pd.Timedelta(step, unit='D')
    microstep_timedelta = pd.Timedelta(1, unit = 's')
    
    times_in_range = []
    while current_time <= pd_end_time:
        next_time = current_time+step_timedelta
        times_in_range.append([to_yt_time(current_time+microstep_timedelta), to_yt_time(next_time)])
        current_time = next_time

    times_in_range = times_in_range[:-1]

    if end_behavior == 'clip':
        return times_in_range
    elif end_behavior == 'full_length':
        times_in_range.append([to_yt_time(current_time-step_timedelta+microstep_timedelta), to_yt_time(pd_end_time)])
        return times_in_range
