import yaml
import numpy as np
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import re
from functools import reduce

def heatMap(fileList, geometryJson):
    f = open(fileList, "r")

    f1 = open (geometryJson.strip(), "r")
    geometryDict = json.loads(f1.read())

    coords = list(map(list, zip(*list(geometryDict.values()))))
    xMax = round(max(coords[0]))+1
    yMax = round(max(coords[1]))+1

    #print(xMax, yMax)

    for file in f:
        f2 = open ('good_jsons/'+file.strip(), "r")
        out = json.loads(f2.read())
        #out = list(map(lambda x: (x[0], np.mean(x[2]), np.std(x[2])), out))

        runNo = re.search(r'\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d',file.strip()).group(0)

        heatMap = np.zeros((xMax, yMax))
        
        #for channel in geometryDict:
        #    try:
        #        heatMap[round(geometryDict[channel][0])][round(geometryDict[channel][1])] = 2  
        #    except:
        #        continue
        for channel in out:
            try:
                #geometryDict[str(channel[0])]i
                heatMap[round(geometryDict[str(channel[0])][0])][round(geometryDict[str(channel[0])][1])] = channel[1]
            except KeyError:
               continue

            #heatMap[round(geometryDict[str(channel[0])][1])][round(geometryDict[str(channel[0])][0])] = channel[1]

        #print(1.0 - ( np.count_nonzero(heatMap) / float(heatMap.size) ))

        #fig, ax = plt.subplots()
        fig = plt.figure(figsize=[16, 7])

        ax = sns.heatmap(heatMap, vmin=65, vmax=95)
        #im = ax.imshow(heatMap)
        plt.xlim(-630,630)
        plt.ylim(-330,330)
        plt.savefig(f"plots/other_geometry/{runNo}_heat.png", transparent=True)
        #plt.show()
        plt.close()

if __name__ == '__main__':
    heatMap(sys.argv[1], sys.argv[2])

