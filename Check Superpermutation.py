import itertools

superperm = '123132132312'

N = len(set(superperm))

permutations = [''.join([str(char) for char in tup]) for tup in list(itertools.permutations([i + 1 for i in range(N)]))]

if all(True if perm in superperm else False for perm in permutations):
    print(f'SUCCESS!\n{superperm} is a Superpermutation of N = {N}\nThe new Superpermutation has length {len(superperm)}')
else:
    print(f'FAIL!\n{superperm} is not a SUperpermutation of N = {N}')