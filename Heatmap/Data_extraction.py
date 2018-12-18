import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Desert_death = {}
Erangel_death = {}
Savage_death = {}

Desert_weapon = {}
Erangel_weapon = {}
Savage_weapon = {}

Desert_use  = {}
Erangel_use = {}
Savage_use = {}

d = 0
w = 0
u = 0
m = 0

for i in range(2,6):
    filename = "./6893/project/process/data/Miramar/telemetry" + str(i) + ".json"
    f = open(filename, 'r')
    line = f.readline()
    while line:
        data = json.loads(line.strip("\n"))
        m += 1
        death_position = {}
        weapon_pickup = {}
        use_pickup = {}
        for item in data:
            indicator = item["_T"]
            if indicator == "LogMatchStart":
                map_name = item["mapName"]
                
            if indicator == "LogPlayerKill":
                death = {}
                death["match"] = m
                death["matchName"] = map_name
                death["x"] = item["victim"]["location"]["x"]/100
                death["y"] = item["victim"]["location"]["y"]/100
                death_position[d] = death
                d += 1
                
            if indicator == "LogItemPickup":
                gamePeriod = item["common"]["isGame"]                
                if gamePeriod > 0.1 and gamePeriod < 2.0:
                    cat = item["item"]["category"]
                    if cat == "Weapon":
                        weapon = {}
                        weapon["match"] = m
                        weapon["name"] = item["item"]["itemId"].split("_")[-2]
                        weapon["x"] = item["character"]["location"]["x"]/100
                        weapon["y"] = item["character"]["location"]["y"]/100
                        weapon_pickup[w] = weapon
                        w += 1
                    if cat == "Use":
                        use = {}
                        use["match"] = m
                        use["name"] = item["item"]["itemId"].split("_")[-2]
                        use["x"] = item["character"]["location"]["x"]/100
                        use["y"] = item["character"]["location"]["y"]/100
                        use_pickup[u] = use
                        u += 1
                        
        if map_name == "Desert_Main":
            Desert_death.update(death_position)
            Desert_weapon.update(weapon_pickup)
            Desert_use.update(use_pickup)
            
        elif map_name == "Erangel_Main":
            Erangel_death.update(death_position)
            Erangel_weapon.update(weapon_pickup)
            Erangel_use.update(use_pickup)
        else:
            Savage_death.update(death_position)
            Savage_weapon.update(weapon_pickup)
            Savage_use.update(use_pickup)
            
        line = f.readline()
    f.close()
    print(i, len(Desert_weapon), len(Erangel_weapon), len(Savage_weapon))

d_desert = pd.DataFrame.from_dict(Desert_death).T
d_erangle = pd.DataFrame.from_dict(Erangel_death).T
d_savage = pd.DataFrame.from_dict(Savage_death).T

w_desert = pd.DataFrame.from_dict(Desert_weapon).T
w_erangle = pd.DataFrame.from_dict(Erangel_weapon).T
w_savage = pd.DataFrame.from_dict(Savage_weapon).T

u_desert = pd.DataFrame.from_dict(Desert_use).T
u_erangle = pd.DataFrame.from_dict(Erangel_use).T
u_savage = pd.DataFrame.from_dict(Savage_use).T

d_desert.to_csv('desert_death.csv')
d_erangle.to_csv('erangel_death.csv')
d_savage.to_csv('savage_death.csv')

w_desert.to_csv('desert_weapon.csv')
w_erangle.to_csv('erangel_weapon.csv')
w_savage.to_csv('savage_weapon.csv')

u_desert.to_csv('desert_use.csv')
u_erangle.to_csv('erangel_use.csv')
u_savage.to_csv('savage_use.csv')
