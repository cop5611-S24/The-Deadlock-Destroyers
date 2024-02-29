import pandas as pd
import itertools
import subprocess
import os
import time

settings = {
  # brightness at 0%, 20%...100%
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

for i in range(len(device_brightness_percentages)):
  device_brightness_percentages[i] = round(device_brightness_percentages[i])

print(device_brightness_percentages)

tempres = ""
for dbp in device_brightness_percentages:
  # ---------- CONFIGURATION COMMANDS GO HERE ----------
  print(f"adb shell settings put system screen_brightness {dbp}")
  subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", str(dbp)], capture_output=True, text=True)
  # get battery life
  battery_dump = subprocess.run(["adb", "shell", "dumpsys", "battery"], capture_output=True, text=True).stdout
  # Get charge counter
  charge_counter = int(battery_dump.split("Charge counter: ")[1].split("\n")[0])
  print(f"Charge counter: {charge_counter}")
  # ----------------------------------------------------

  # ---------- MEASUREMENT COMMANDS GO HERE ------------
  current_battery_level = int(battery_dump.split("level: ")[1].split("\n")[0])
  print(f"Current battery level: {current_battery_level}")

  current_time = time.time()
  print(f"Current time: {current_time}")
  # ----------------------------------------------------

  # ---------- DATA STORAGE COMMANDS GO HERE -----------
  # tempres += f"{current_time},{current_battery_level},{dbp}\n"
  # Store data in first two columns of data frame
  # ----------------------------------------------------
  time.sleep(5)


# with open("output.csv", "w") as f:
#  adb shell am start -a android.intent.action.VIEW spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play
# result = subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play"], capture_output=True, text=True)
# print(result.stdout)
