import itertools


def generate_permutations(n):
    nList = []

    for i in range(n):
        nList.append(i+1)

    # calculate all permutations
    permutations = list(itertools.permutations(nList))

    if verboseMode: print(permutations)
    return permutations


def convertTuple(tup):
    str1 =  ''.join(str(e) for e in tup)
    return str1

def readFile(dict):
    file = open("superpermutations.txt", "r")

    keyFlag = False
    for val in file.read().split():

        if keyFlag:
            if key in dict:
                dict[key].append(int(val))

            else:
                dict[key] = [int(val)]
            keyFlag = False

        if int(val) < 121:
            keyFlag = True
            key = int(val)

    file.close()
    return dict

#   MAIN

verboseMode = False

N = 4
DICT_INDEX = 1

dictionary = {}

dictSuperPermutations = readFile(dictionary)

strSuper = (str)(dictSuperPermutations[N][DICT_INDEX])

permutations = generate_permutations(N)

success = False
permMatchCount = 0


for i in permutations:
    tup = convertTuple(i)
    if verboseMode: print('Searching for: ', tup)

    for j in range(len(strSuper)):
        if verboseMode: print('String position ', j)

        charMatchCount = 0
        for k in range(N):
            if verboseMode: print('Character test', k)

            if strSuper[j + k] == tup[k]:
                if verboseMode: print ('Character match: ', strSuper[j + k], ' = ', tup[k])
                charMatchCount += 1

        if charMatchCount == N:
            permMatchCount += 1
            if verboseMode: print('PERMUTATION MATCH FOUND')
            break

    if permMatchCount == len(permutations):
        success = True

if success:
    print('SUCCESS: ', strSuper, ' IS A SUPERPERMUTATION OF N = ', N)
else:
    print('FAIL: ', strSuper, ' IS NOT A SUPERPERMUTATION OF N = ', N)

