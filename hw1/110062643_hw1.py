import sys
from apyori import apriori # for test
from collections import Counter


def apriori_myself(transations, min_support):
    association_results = []
    init = []

    for transation in transations:
        for t in transation:
            if t not in init:
                init.append(t)

    # sort init
    init = [int(x) for x in init]
    init = sorted(init)
    init = [str(x) for x in init]

    s = int(min_support * len(init))    #calculate iteration

    c = Counter()
    for i in init:
        for transation in transations:
            if i in transation:
                c[i] += 1
    print('C1:')
    for i in c:
        print(str(i)+ ':' +str(c[i]))

    return association_results


# read data
data = []
results = []
with open(sys.argv[2], 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.rstrip().split(',')
        data.append(line)

mim_support = float(sys.argv[1])

results = apriori_myself(data, mim_support)
# association_rules = apriori(data, min_support=float(sys.argv[1]))
# association_results = list(association_rules)

# for item in association_results:
#     pair = item[0]
#     items = [x for x in pair]
#     items = ','.join(sorted(items))
#     support = float(item[1])
#     results.append(items + ':' + '%.04f'%support)

# output file
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    for result in results:
        f.write(result+'\n')