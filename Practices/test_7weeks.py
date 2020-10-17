
def gcd(a, b):
    if a < b:
        a, b = b, a
    if a % b == 0:
        return b
    return gcd(b, a % b)
print(gcd(12, 34))

def lcm(a, b):
    return a * b / gcd(a, b)
print(lcm(12, 34))


from itertools import permutations
from itertools import combinations

import time

# 순열(combination) & 조합(permutation)
n = [1, 2, 3, 4]
m = 2

a = []
start = time.time()
print("순열")
for i in list(combinations(n, m)):
    a.append(i)
print(a)
print(time.time() - start)

b = []
start = time.time()
for i in list(permutations(n, m)):
    b.append(i)
print(b)
print(time.time() - start)