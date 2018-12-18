import json
import csv
import pandas as pd

players = {}
i = 0
for line in open('C:\\Users\Yin Hang\Downloads\\match.json', 'r'):
    data = json.loads(line)

    # data of each game
    if 'included' in data.keys():
        for e in data['included']:
            if 'stats' in e['attributes'].keys():
                # print(json.dumps(e['attributes']['stats'],indent=1))
                if 'DBNOs' in e['attributes']['stats'].keys():
                    # write the certain fields into csv file
                    keys = list(e['attributes']['stats'].keys())
                    players[i] = e['attributes']['stats']
                    i = i + 1


df = pd.DataFrame.from_dict(players).T
df.to_csv('C:\\Users\Yin Hang\Desktop\\match.csv')
