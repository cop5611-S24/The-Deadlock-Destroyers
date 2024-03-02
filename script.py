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

df = pd.DataFrame(columns=["timestamp", "currentCharge"] + list(settings.keys()))
# Now we need to populate the dataframe with all the possible combinations.
for combination in itertools.product(*settings.values()):
  df = df._append(pd.Series([None, None] + list(combination), index=df.columns), ignore_index=True)

def configure_device(brightness, wifi, bluetooth, gps, power_saving, refresh_rate, game_enabled, video_playing_resolution, browsing, music_playing):
  # brightness
  device_max_sreen_brightness_range = [22, 4095]
  device_brightness = (brightness / 100) * (device_max_sreen_brightness_range[1] - device_max_sreen_brightness_range[0]) + device_max_sreen_brightness_range[0]
  device_brightness = round(device_brightness)
  print(f"adb shell settings put system screen_brightness {device_brightness}")
  subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", str(device_brightness)], capture_output=True, text=True)

  # wifi
  if wifi == 0:
    print("adb shell svc wifi disable")
    subprocess.run(["adb", "shell", "svc", "wifi", "disable"], capture_output=True, text=True)
  else:
    print("adb shell svc wifi enable")
    subprocess.run(["adb", "shell", "svc", "wifi", "enable"], capture_output=True, text=True)

  # bluetooth
  if bluetooth == 0:
    print("adb shell svc bluetooth disable")
    subprocess.run(["adb", "shell", "svc", "bluetooth", "disable"], capture_output=True, text=True)
  else:
    print("adb shell svc bluetooth enable")
    subprocess.run(["adb", "shell", "svc", "bluetooth", "enable"], capture_output=True, text=True)

  # gps
  if gps == 0:
    print("adb shell settings put secure location_providers_allowed -gps")
    subprocess.run(["adb", "shell", "settings", "put", "secure", "location_providers_allowed", "-gps"], capture_output=True, text=True)
  else:
    print("adb shell settings put secure location_providers_allowed +gps")
    subprocess.run(["adb", "shell", "settings", "put", "secure", "location_providers_allowed", "+gps"], capture_output=True, text=True)

  # power_saving
  if power_saving == 0:
    print("adb shell settings put global low_power 0")
    subprocess.run(["adb", "shell", "settings", "put", "global", "low_power", "0"], capture_output=True, text=True)
  else:
    print("adb shell settings put global low_power 1")
    subprocess.run(["adb", "shell", "settings", "put", "global", "low_power", "1"], capture_output=True, text=True)

  # refresh_rate
  print(f"adb shell settings put system peak_refresh_rate {refresh_rate}")
  subprocess.run(["adb", "shell", "settings", "put", "system", "peak_refresh_rate", str(refresh_rate)], capture_output=True, text=True)

  print(f"adb shell settings put system min_refresh_rate {refresh_rate}")
  subprocess.run(["adb", "shell", "settings", "put", "system", "min_refresh_rate", str(refresh_rate)], capture_output=True, text=True)

  if (browsing == 0):
    print("adb shell am force-stop com.android.chrome")
    subprocess.run(["adb", "shell", "am", "force-stop", "com.android.chrome"], capture_output=True, text=True)
  else:
    print("adb shell am start -a android.intent.action.VIEW -d http://www.twitter.com")
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "http://www.twitter.com"], capture_output=True, text=True)
  
  if (music_playing == 0):
    print("adb shell am force-stop com.spotify.music")
    subprocess.run(["adb", "shell", "am", "force-stop", "com.spotify.music"], capture_output=True, text=True)
  else:
    print("adb shell am start -a android.intent.action.VIEW spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play")
    subprocess.run(["adb", "shell" , "am", "start", "-a", "android.intent.action.VIEW", "spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play"])



device_max_sreen_brightness_range = [22, 4095]
device_brightness_percentages = []
for brightness_level in settings["brightness"]:
  device_brightness_percentages.append((brightness_level / 100) * (device_max_sreen_brightness_range[1] - device_max_sreen_brightness_range[0]) + device_max_sreen_brightness_range[0])

for i in range(len(device_brightness_percentages)):
  device_brightness_percentages[i] = round(device_brightness_percentages[i])

print(device_brightness_percentages)

# In case the script needs to be stopped, use this variable to know where to start from
iteration_counter = 1
tempres = ""

# Loop through each row in the dataframe
# Use the values from the 3rd column onwards to configure the device
# Measure the battery life
# Store the results in a file
# Sleep for 2 minutes.
# Repeat
for index, row in df.iterrows():

  # ---------- CONFIGURATION COMMANDS GO HERE ----------
  configure_device(*row[2:])
  # print configurations to terminal for debugging
  print(f"brightness: {row[2]}, wifi: {row[3]}, bluetooth: {row[4]}, gps: {row[5]}, power_saving: {row[6]}, refresh_rate: {row[7]}, game_enabled: {row[8]}, video_playing_resolution: {row[9]}, browsing: {row[10]}, music_playing: {row[11]}")
  # ----------------------------------------------------

  # ---------- MEASUREMENT COMMANDS GO HERE ------------
  # get battery life
  battery_dump = subprocess.run(["adb", "shell", "dumpsys", "battery"], capture_output=True, text=True).stdout
  # Get charge counter
  charge_counter = int(battery_dump.split("Charge counter: ")[1].split("\n")[0])
  print(f"Charge counter: {charge_counter}")
  current_battery_level = int(battery_dump.split("level: ")[1].split("\n")[0])
  print(f"Current battery level: {current_battery_level}")

  current_time = time.time()
  print(f"Current time: {current_time}")
  # ----------------------------------------------------

  # ---------- DATA STORAGE COMMANDS GO HERE -----------
  tempres += f"{current_time},{current_battery_level}, Iteration: {iteration_counter}\n"

  # ----------------------------------------------------

  iteration_counter += 1
  time.sleep(5)


# with open("output.csv", "w") as f:
#  adb shell am start -a android.intent.action.VIEW spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play
# result = subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play"], capture_output=True, text=True)
# print(result.stdout)
