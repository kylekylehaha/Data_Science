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

    s = int(min_support * len(init))    # mim support count

    c = Counter()
    for i in init:
        for transation in transations:
            if i in transation:
                c[i] += 1
    print('C1:')
    for i in c:
        print(str(i)+ ':' + str(c[i]))
    print()

    l = Counter()
    for i in c:
        if c[i] >= s:
            l[frozenset([i])] += c[i]

    print('L1:')
    for i in l:
        print(str(i) + ':' + str(l[i]))
    print()

    pl = 1
    pos = 1

    for count in range(2, 1000):
        nc = set()
        temp = list(l)
        for i in range(0, len(temp)):
            for j in range(i+1, len(temp)):
                t = temp[i].union(temp[j])
                if len(t) == count:
                    nc.add(temp[i].union(temp[j]))

        nc = list(nc)
        c = Counter()
        for i in nc:
            c[i] = 0
            for transation in transations:
                temp = set(transation)
                if i.issubset(temp):
                    c[i] += 1
        print('C' + str(count) + ':')
        for i in c:
            print(str(i) + ':' +str(c[i]))
        print()

        l = Counter()
        for i in c:
            if(c[i] >= s):
                l[i]+=c[i]
        print("L"+str(count)+":")
        for i in l:
            print(str(list(i))+": "+str(l[i]))
        print()

        if len(l) == 0:
            break
        
        pl = l
        pos = count

    print("Result: ")
    print("L"+str(pos)+":")
    for i in pl:
        print(str(list(i))+": "+str(pl[i]))
    print()

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