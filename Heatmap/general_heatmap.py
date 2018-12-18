import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.misc.pilutil import imread
from scipy.ndimage.filters import gaussian_filter
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import argparse

parser = argparse.ArgumentParser(description='Declare the map and category.')
parser.add_argument('map',type=int, choices=range(0,3),help="An integer to declare the map genre: 0-Erangel, 1-Miramar, 2-Savage")
parser.add_argument('category',type=int, choices =range(0,3),help="An integer to declare the category of the data: 0-death, 1-weapon, 2-medicine")

args = parser.parse_args()

mapName = ['erangel','miramar','savage']
categoryName = ['death', 'weapon', 'use']
mapSize = [8160, 8160, 4080]

file = "./extraction_data/" + mapName[args.map] + '/' + mapName[args.map] + '_' + categoryName[args.category] + '.csv'
bg_file = './figure/' + mapName[args.map] + '.png' 
df = pd.read_csv(file)
bg = imread(bg_file)

df.x = df.x*(bg.shape[0])/mapSize[args.map]
df.y = df.y*(bg.shape[1])/mapSize[args.map]

def heatmap(x, y, s, bins=100):
	heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
	heatmap = gaussian_filter(heatmap, sigma=s)
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
	return heatmap.T, extent

if args.category == 0:
	hmap, extent = heatmap(df.x, df.y, 1.5, bins=800)
	minValue = hmap.max()/200
	maxValue = hmap.max()/20
elif args.category == 1:
	Kar98 = df.loc[df.name == 'Kar98k']
	HK416 = df.loc[df.name == 'HK416']
	hmap1, extent = heatmap(Kar98.x, Kar98.y, 1.5, bins=800)
	hmap2, extent = heatmap(HK416.x, HK416.y, 1.5, bins=800)
	hmap3, extent = heatmap(df.x, df.y, 1.5, bins=800)
	hmap = 3*hmap1 + 3*hmap2 + hmap3
	minValue = hmap.max()/200
	maxValue = hmap.max()
else:
	MedKit = df.loc[df.name=="MedKit"]
	Adrenaline = df.loc[df.name=="AdrenalineSyringe"]
	FirstAid = df.loc[df.name=="FirstAid"]
	hmap1, extent = heatmap(MedKit.x, MedKit.y, 1.5, bins=800)
	hmap2, extent = heatmap(Adrenaline.x, Adrenaline.y, 1.5, bins=800)
	hmap3, extent = heatmap(FirstAid.x, FirstAid.y, 1.5, bins=800)
	hmap4, extent = heatmap(df.x, df.y, 1.5, bins=800)
	hmap = 500*hmap1 + 500*hmap2 + hmap4
	minValue = hmap.max()/100
	maxValue = hmap.max()/10

hmap, extent = heatmap(df.x, df.y, 1.5, bins=800)
alphas = np.clip(Normalize(0, minValue, clip=True)(hmap)*1.5, 0.0, 1.)
colors = Normalize(minValue, maxValue, clip=True)(hmap)
colors = cm.bwr(colors)
colors[..., -1] = alphas
fig, ax = plt.subplots()
ax.set_xlim(0, bg.shape[0])
ax.set_ylim(0, bg.shape[1])
ax.imshow(bg)
ax.imshow(colors, extent=extent, origin='lower', cmap=cm.bwr, alpha=0.7)
plt.gca().invert_yaxis()
plt.show()