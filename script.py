import pandas as pd
import itertools
import subprocess
import os
import time

settings = {
  # application workloads are mutually exclusive
  "application_workload": ["none", "game", "video720", "video1080", "browsing", "music"],
  "brightness": [0, 20, 40, 60, 80, 100],
  "bluetooth": [0, 1],
  "gps": [0, 1],
  "power_saving": [0, 1],
  "refresh_rate": [60, 120],
  # wifi always on because we need to debug via adb wirelessly
}

#df = pd.DataFrame(columns=["timestamp", "currentCharge"] + list(settings.keys()))
# Now we need to populate the dataframe with all the possible combinations.
#for combination in itertools.product(*settings.values()):
#  df = df._append(pd.Series([None, None] + list(combination), index=df.columns), ignore_index=True)
df = pd.read_csv("output.csv")

def run_workload(workload):
  # need to confirm that these work
  if (workload == "browsing"):
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "http://www.twitter.com"], capture_output=True, text=True)
  elif (workload == "music"):
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play"], capture_output=True, text=True)
  elif (workload == "game"):
    subprocess.run(["adb", "shell", "am", "start",  "-n", "com.rovio.baba/com.unity3d.player.UnityPlayerActivity"], capture_output=True, text=True)
  elif (workload == "video720"):
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "http://www.youtube.com/watch?v=YRhFSWz_J3I", "--ei", "resolution", "720"], capture_output=True, text=True)
  elif (workload == "video1080"):
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "http://www.youtube.com/watch?v=YRhFSWz_J3I", "--ei", "resolution", "1080"], capture_output=True, text=True)

def configure_device(workload, brightness, bluetooth, gps, power_saving, refresh_rate):
  # brightness
  device_max_sreen_brightness_range = [22, 4095]
  device_brightness = (brightness / 100) * (device_max_sreen_brightness_range[1] - device_max_sreen_brightness_range[0]) + device_max_sreen_brightness_range[0]
  device_brightness = round(device_brightness)
  print(f"adb shell settings put system screen_brightness {device_brightness}")
  print( subprocess.run(["adb", "shell", "settings", "put", "system", "screen_brightness", str(device_brightness)], capture_output=True, text=True).stdout)

  # bluetooth
  # May need to forget about BT because it's not working
  print(f"adb shell settings put global bluetooth_disabled_profiles {bluetooth}")
  print( subprocess.run( ["adb", "shell", "settings", "put", "global", "bluetooth_disabled_profiles", f"{bluetooth}"], capture_output=True, text=True).stdout)

  # gps
  print(f"adb shell settings put secure location_providers_allowed {'-' if gps == 0 else '+'}gps")
  print (subprocess.run(["adb", "shell", "settings", "put", "secure", "location_providers_allowed", f"{"-" if gps == 0 else "+"}gps"], capture_output=True, text=True).stdout)

  # power_saving
  print(f"adb shell settings put global low_power {"0" if power_saving == 0 else "1"}")
  print(subprocess.run(["adb", "shell", "settings", "put", "global", "low_power", f"{"0" if power_saving == 0 else "1"}"], capture_output=True, text=True).stdout)

  # refresh_rate
  print(f"adb shell settings put system peak_refresh_rate {refresh_rate}")
  if(refresh_rate == 60):
    subprocess.run(["adb", "shell", "settings", "put", "system", "peak_refresh_rate", "60"], capture_output=True, text=True)
  elif(refresh_rate == 120):
    subprocess.run(["adb", "shell", "settings", "put", "system", "peak_refresh_rate", "120"], capture_output=True, text=True)
    subprocess.run(["adb", "shell", "settings", "put", "system", "min_refresh_rate", "120"], capture_output=True, text=True)

  run_workload(workload)


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
df_copy = df.copy()

"""
  Loop through each row in the dataframe
  Use the values from the 3rd column onwards to configure the device
  Measure the battery life
  Store the results in a file
  Sleep for 2 minutes.
  Repeat
"""
for index, row in df.iterrows():

  # ---------- CONFIGURATION COMMANDS GO HERE ----------
  configure_device(*row[2:])
  # print configurations to terminal for debugging
  print(f"Configurations: {row[2:]}")
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
  row['current_time'] = current_time
  row['current_battery_level'] = current_battery_level
  if (index == 0):
      with open("result.csv", "a") as f:
          f.write(','.join(df.columns) + '\n')

  # row_string = str(row['current_time']) + "," + str(row["current_battery_level"]) + "," + str(row["brightness"]) + "," + str(row["wifi"]) + "," + str(row["bluetooth"]) + "," + str(row["gps"]) + "," + str(row["power_saving"]) + "," + str(row["refresh_rate"]) + "," + str(row["game_enabled"]) + "," + str(row["video_playing_resolution"]) + "," + str(row["browsing"]) + "," + str(row["music_playing"]) + "\n"
  row_string = ','.join([str(x) for x in row]) + '\n'

  with open("result.csv", "a") as f:
      f.write(row_string)
  # ----------------------------------------------------

  print(f"Iteration: {iteration_counter}")
  iteration_counter += 1
  time.sleep(10)
  # exit(0)


# with open("output.csv", "w") as f:
#  adb shell am start -a android.intent.action.VIEW spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play
# result = subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "spotify:playlist:4bfj9Go9YnSq7L4YeWTWeY:play"], capture_output=True, text=True)
# print(result.stdout)
