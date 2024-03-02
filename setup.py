#! /usr/bin/python

import pandas as pd
import itertools

settings = {
  "brightness": [0, 20, 40, 60, 80, 100],
  "wifi": [0, 1],
  "bluetooth": [0, 1],
  "gps": [0, 1],
  "power_saving": [0, 1],
  "refresh_rate": [60, 120],
  "game_enabled": [0, 1],
  "video_playing_resolution": ["720p", "1080p"],
  "browsing": [0, 1],
  "music_playing": [0, 1]
}

# First step is to populate the dataframe with all the possible combinations
# Leave the first 2 columns empty for the timestamp and the currentCharge

df = pd.DataFrame(columns=["timestamp", "currentCharge"] + list(settings.keys()))

# Now we need to populate the dataframe with all the possible combinations.

for combination in itertools.product(*settings.values()):
  df = df._append(pd.Series([None, None] + list(combination), index=df.columns), ignore_index=True)

# print dataframe as csv

df.to_csv("output.csv", index=False)
