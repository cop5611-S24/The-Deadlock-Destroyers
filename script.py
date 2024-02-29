import pandas as pd
import itertools
import subprocess
import os

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

device_max_sreen_brightness_range = [22, 4095]
device_brightness_percentages = []
for brightness_level in settings["brightness"]:
  device_brightness_percentages.append((brightness_level / 100) * (device_max_sreen_brightness_range[1] - device_max_sreen_brightness_range[0]) + device_max_sreen_brightness_range[0])

print(device_brightness_percentages)

# Open output.csv file

# with open("output.csv", "w") as f:
#  adb shell am start -a android.intent.action.VIEW spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play
result = subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play"], capture_output=True, text=True)

print(result.stdout)
