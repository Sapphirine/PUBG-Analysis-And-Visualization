import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ### Dynamic Match: visualize real-time players' positions and zones' positions

# ### 1 Extract telemetry data of a match from json file
Name = "Erangel" # "Savage", "Desert"
for i in range(2, 3):
    filename = "telemetry" + str(i) + ".json"
    f = open(filename, 'r')
    line = f.readline()
    while line:
        data = json.loads(line.strip("\n"))
        for item in data:
            indicator = item["_T"]
            if indicator == "LogMatchStart":
                map_name = item["mapName"]
                teamSize = item["teamSize"]
                if map_name == Name + "_Main":
                     dat = data
        line = f.readline()
    f.close()


# ### 2 Extract player and zone statistics from telemetry data
player_killed = {}
player_position = {}
zone = {}
k = 0
po = 0
z = 0
totalNum = 100

for item in dat:
    indicator = item["_T"]
    # players killed
    if indicator == "LogPlayerKill":
        player = {}
        # death timestamp
        player["time"] = item["_D"][11:19]
        # player ID
        player["ID"] = item["victim"]["accountId"]
        # current number of players alive
        player["number_alive"] = totalNum - k
        # players positions
        player["x"] = item["victim"]["location"]["x"]/100
        player["y"] = item["victim"]["location"]["y"]/100
        player["health"] = 0
        player_killed[k] = player
        k += 1

    if indicator == "LogPlayerPosition":
        position = {}
        position["time"] = item["_D"][11:19]
        position["ID"] = item["character"]["accountId"]
        position["number_alive"] = item["numAlivePlayers"]
        position["health"] = item["character"]["health"]
        position["x"] = item["character"]["location"]["x"]/100
        position["y"] = item["character"]["location"]["y"]/100
        player_position[po] = position
        po += 1

    if indicator == "LogGameStatePeriodic":
        game ={}
        game["time"] = item["_D"][11:19]
        # blue zone 
        game["blue_x"] = item["gameState"]["safetyZonePosition"]["x"]/100
        game["blue_y"] = item["gameState"]["safetyZonePosition"]["y"]/100
        game["blue_r"] = item["gameState"]["safetyZoneRadius"]/100
        # safe zone
        game["safe_x"] = item["gameState"]["poisonGasWarningPosition"]["x"]/100
        game["safe_y"] = item["gameState"]["poisonGasWarningPosition"]["y"]/100
        game["safe_r"] = item["gameState"]["poisonGasWarningRadius"]/100
        
        zone[z] = game
        z += 1

k, po, z


# ### 3 Compute the duration of a timestamp from the beginning of the match
from datetime import datetime
fmt = "%H:%M:%S"
# beginning of a match as base time
base_time = datetime.strptime(zone[0]["time"], fmt)

for i in player_killed:
    time = player_killed[i]["time"]
    interval = datetime.strptime(time, fmt) - base_time
    player_killed[i]["duration"] = interval.seconds
    
for i in player_position:
    time = player_position[i]["time"]
    interval = datetime.strptime(time, fmt) - base_time
    player_position[i]["duration"] = interval.seconds
    
for i in zone:
    time = zone[i]["time"]
    interval = datetime.strptime(time, fmt) - base_time
    zone[i]["duration"] = interval.seconds


# ### 4 Convert player and zone data to csv files
df = pd.DataFrame.from_dict(player_position).T
split = [i for i, x in enumerate(np.array(df["time"] == zone[0]["time"])) if x][-1]
df = df.iloc[split:]

df_player_killed = pd.DataFrame.from_dict(player_killed).T

df_zone = pd.DataFrame.from_dict(zone).T
df_zone.to_csv(Name + "_zone.csv")

df_position = df.append(df_player_killed, ignore_index=True).sort_values(["duration"])
unique_names = np.unique(np.array(df_position["ID"]))
for i, name in enumerate(unique_names):
    df_position.replace(name, i, inplace=True)
    
split = [i for i, x in enumerate(np.array(df_position["duration"] == 20)) if x][-1]
df_position.iloc[split:].to_csv(Name + "_position.csv")



