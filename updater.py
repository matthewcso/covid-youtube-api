# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
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

output_folder = output_dir
target_folder = output_dir

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

for week in os.listdir(target_folder):
    this_week_data = pd.read_csv(os.path.join(target_folder, week))
    new_df = pd.DataFrame()
    if len(this_week_data['videoId']) >= 1:
        updated_week_data = youtube_videos(list(this_week_data['videoId']), youtube)
        ids = updated_week_data[7]

        for i, row in this_week_data.iterrows():
            try:
                indexer = ids.index(row['videoId'])

                this_week_data['viewCount'][indexer] = updated_week_data[1][indexer]
                this_week_data['likeCount'][indexer] = updated_week_data[2][indexer]
                this_week_data['dislikeCount'][indexer] = updated_week_data[3][indexer]
                this_week_data["commentCount"][indexer] = updated_week_data[4][indexer]

            except ValueError:

                this_week_data['viewCount'][i] = -1*row['viewCount']
                this_week_data['likeCount'][i] = -1*row['likeCount'] 
                this_week_data['dislikeCount'][i] = -1*row['dislikeCount']
                this_week_data["commentCount"][i] = -1*row["commentCount"]

    this_week_data.to_csv(os.path.join(output_folder, week))




# %%
