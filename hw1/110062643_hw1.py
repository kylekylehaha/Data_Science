import sys
from apyori import apriori # for test

data = []
with open(sys.argv[2], 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.rstrip().split(',')
        data.append(line)
    
    # print(data)
    # print(data1)
    # data2 = [['r', 'z', 'h', 'j', 'p'],
    #    ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #    ['z'],
    #    ['r', 'x', 'n', 'o', 's'],
    #    ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #    ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # print(type(data2[0][0]))
    association_rules = apriori(data, min_support=float(sys.argv[1]))
    association_results = list(association_rules)

    print(len(association_results))
    results = []
    for item in association_results:
        pair = item[0]
        items = [x for x in pair]
        items = ','.join(sorted(items))
        support = float(item[1])
        results.append(items + ':' + '%.04f'%support)

    print(results)
    # for item in association_results:
    #     pair = item[0] 
    #     items = [x for x in pair]
    #     print("Rule: " + items[0] + " -> " + items[1])
    #     print("Support: " + str(item[1]))
    #     print("Confidence: " + str(item[2][0][2]))
    #     print("Lift: " + str(item[2][0][3]))
    #     print("=====================================")