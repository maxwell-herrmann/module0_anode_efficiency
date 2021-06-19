import yaml
import numpy as np
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import re
from functools import reduce
import h5py

def unique_channel_id(io_group, io_channel, chip_id, channel_id):
    return channel_id + 64*(chip_id + 256*(io_channel+256*io_group))

def heatMap(dataFile, geometryJson):
    f = h5py.File(dataFile, "r")
    g = open (geometryJson.strip(), "r")
    geometryDict = json.loads(g.read())

    coords = list(map(list, zip(*list(geometryDict.values()))))
    xMax = round(max(coords[0]))+1
    xMin = round(min(coords[0]))-1
    yMax = round(max(coords[1]))+1
    yMin = round(min(coords[1]))-1

    print(xMax, yMax)
    print(xMin, yMin)
    runNo = re.search(r'\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d',dataFile.strip()).group(0)

    heatMap = np.zeros((xMax-xMin, yMax-yMin))
    heatMap2 = np.zeros((xMax-xMin, yMax-yMin))    
    #for channel in geometryDict:
    #    try:
    #        heatMap[round(geometryDict[channel][0])][round(geometryDict[channel][1])] = 2  
    #    except:
    #        continue

    counting=0
    total=len(f['hits'])
    for i in range(0, 10000000):
    #for hit in f['hits']:
        counting+=1
        hit=f['hits'][i]
        unique=str(unique_channel_id(hit['iogroup'], hit['iochannel'], hit['chipid'], hit['channelid']))
        try:
            #geometryDict[str(channel[0])]
            heatMap[round(geometryDict[unique][0])-xMin][round(geometryDict[unique][1])-yMin] += 1
            heatMap2[round(geometryDict[unique][0]-xMin)][round(geometryDict[unique][1])-yMin] += hit['q']
        except KeyError:
           continue

        #heatMap[round(geometryDict[str(channel[0])][1])][round(geometryDict[str(channel[0])][0])] = channel[1]
        
        if counting % 100000 == 0:
            print(f'we have done {counting} out of {total}.')

    #print(1.0 - ( np.count_nonzero(heatMap) / float(heatMap.size) ))

    #fig, ax = plt.subplots()
    fig = plt.figure(figsize=[20, 10])

    ax = sns.heatmap(heatMap, cmap='viridis', robust=True)
    #im = ax.imshow(heatMap)
    #plt.xlim(-630,630)
    #plt.ylim(-330,330)
    #plt.savefig(f"plots/other_geometry/{runNo}_heat.png", transparent=True)
    plt.show()
    plt.close()

    fig=plt.figure(figsize=[20,10])
    ax=sns.heatmap(heatMap2, cmap='viridis', robust=True)
    plt.show()
    plt.close()

if __name__ == '__main__':
    heatMap(sys.argv[1], sys.argv[2])

