import sys
import time
from utils import *
from collections import defaultdict
from itertools import chain, combinations

def getFromFile(fname):
    itemSetList = []
    frequency = []
    
    with open(fname, 'r') as file:
        for line in file.readlines():
            line = line.rstrip().split(',')
            itemSetList.append(line)
            frequency.append(1)

    return itemSetList, frequency

def fpgrowthFromFile(fname, minSupRatio):
    itemSetList, frequency = getFromFile(fname)
    minSup = len(itemSetList) * minSupRatio
    fpTree, headerTable = constructTree(itemSetList, frequency, minSup)
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        mineTree(headerTable, minSup, set(), freqItems)
        results = output(freqItems, itemSetList, minSup)
        return freqItems, results

def writeFile(fname, results):
    with open(fname, 'w') as f:
        for r in results:
            f.write('{}:{}\n'.format(','.join(list(r[0])), r[1]))

def sorted_writeFile(fname, results):
    tmp = results.copy()
    tmp_r = []
    for t in tmp:
        tmp_list = [int(i) for i in list(t[0])]
        tmp_list.sort()
        tmp_list = [str(i) for i in tmp_list]
        tmp_str = ','.join(tmp_list)
        tmp_r.append([tmp_str, t[1]])
    tmp_r.sort(key= lambda t: t[0], reverse=False)
    tmp_r.sort(key= lambda t: len(t[0]), reverse=False)
    with open(fname, 'w') as f:
        for r in tmp_r:
            f.write('{}:{}\n'.format(r[0], r[1]))

if __name__ == "__main__":
    inputFile = sys.argv[2]
    outFile = sys.argv[3]
    minSup = float(sys.argv[1])

    start = time.time()

    freqItemSet, results = fpgrowthFromFile(inputFile, minSup)

    # writeFile(outFile, results)
    sorted_writeFile(outFile, results)
    print('Time:{}'.format(time.time()-start))