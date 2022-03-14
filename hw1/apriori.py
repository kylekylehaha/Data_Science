import sys
import time
from itertools import combinations

start = time.time()

# Read data
datas = []
with open(sys.argv[2], 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.rstrip().split(',')
        datas.append(line)
data_sets = [set(d) for d in datas]

# Find all item
init = []
for data in datas:
    for d in data:
        if d not in init:
            init.append(d)

init = [int(x) for x in init]
init = sorted(init)
init = [set({str(x)}) for x in init]

# min_support and min_support count
min_sp = float(sys.argv[1])
min_sp_count = int(min_sp*len(datas))

# calculate support count for any set
def support_count(x):   # x: set
    count = 0
    for data_set in data_sets:
        if x.issubset(data_set):
            count += 1
    return count

# calcuale candidate1 and itemset L1
results = []
candidates1 = []    # [[itemset, support_count], [itemset, support_count], ...,] 
l1 = []
for i in init:
    candidates1.append([i,support_count(i)])

for c in candidates1:
    if c[1] >= min_sp_count:
        l1.append(c)

for l in l1:
    support = l[1]/len(datas)
    if support >= min_sp:
        results.append([l[0], '%.04f'%support])

# Find last subset
# return 上一層 subset. e.g.: {'1','2','3'} return {'1','2'}, {'1','3'}, {'2','3'}
def last_subset(x):
    r = []
    subset_list = list(x)
    for t in list(combinations(subset_list, len(subset_list)-1)):
        r.append(set(t))
    return r

def remove_duplicate(can):
    tmp = []
    for c in can:
        if c not in tmp:
            tmp.append(c)
    return tmp

# Apriori algo
last_itemset = [l[0] for l in l1]
last_l = l1
for count in range (2,1000):
    # print('count:{}'.format(count))
    candidates = []
    common_count = count - 2
    
    # print('Generating candidates ...')
    for t in list(combinations(last_itemset,2)):
        if len(t[0].intersection(t[1])) >= common_count:
            union_set = t[0].union(t[1])
            candidates.append([union_set, support_count(union_set)])

    # print("Finish candidates. len(candidates):{}. Time:{}".format(len(candidates), time.time()-start))
    # print()
    # print("Removing duplicate ...")
    candidates = remove_duplicate(candidates)
    # print("Finish remove duplicate. len(candidate):{}. Time:{}".format(len(candidates), time.time()-start))
    # print()

    # prune
    # print('Pruning ....')
    if count != 2:
        for candidate in candidates:
            candidate_set = candidate[0]
            last_s = last_subset(candidate_set) # return 上一層 subset. e.g.: {'1','2','3'} return {'1','2'}, {'1','3'}, {'2','3'}
            for s in last_s:
                if s not in last_itemset:
                    candidates.remove(candidate)
                    break
    # print('Finsih pruning, len(candidates):{}. Time:{}'.format(len(candidates), time.time()-start))
    # print()

    
    # calculate support count
    # print("Filtering ...")
    itemset = []
    for candidate in candidates:
        can_set = candidate[0]
        sup_count = support_count(can_set)
        if sup_count >= min_sp_count:
            itemset.append([can_set, sup_count])

    # print('Finish filter.')
    
    # append into results
    for l in itemset:
        support = l[1]/len(datas)
        if support >= min_sp:
            results.append([l[0], '%.04f'%support])
    
    last_itemset = [l[0] for l in itemset]

    # print('====================')

    if len(itemset) == 0:
        break

    

# print('Result length:{}'.format(len(results)))

# write file
with open(sys.argv[3], 'w', encoding='utf-8') as f:
    for r in results:
        f.write('{}:{}\n'.format(','.join(list(r[0])), r[1]))