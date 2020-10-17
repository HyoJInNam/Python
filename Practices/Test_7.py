
def gcd(a, b):
    if b < a: a, b = b, a
    if a % b == 0 : return b
    return gcd(b, a%b)

def lcm(a, b):
    return a * b / gcd(a, b)

def comb(lst,n):
	ret = []
	if n > len(lst): return ret
	if n == 1:
		for i in lst:
			ret.append([i])
	elif n>1:
		for i in range(len(lst)-n+1):
			for temp in comb(lst[i+1:],n-1):
				ret.append([lst[i]]+temp)

	return ret

def perm(lst,n):
	ret = []
	if n > len(lst): return ret
	if n==1:
		for i in lst:
			ret.append([i])
	elif n>1:
		for i in range(len(lst)):
			temp = [i for i in lst]
			temp.remove(lst[i])
			for p in perm(temp,n-1):
				ret.append([lst[i]]+p)

	return ret

def dfs_comb(lst,n):
	ret = []
	idx = [i for i in range(len(lst))]

	stack  = []
	for i in idx[:len(lst)-n+1]:
		stack.append([i])

	while len(stack)!=0:
		cur = stack.pop()

		for i in range(cur[-1]+1,len(lst)-n+1+len(cur)):
			temp=cur+[i]
			if len(temp)==n:
				element = []
				for i in temp:
					element.append(lst[i])
				ret.append(element)
			else:
				stack.append(temp)
	return ret

def dfs_perm(lst,n):
	ret = []
	idx = [i for i in range(len(lst))]

	stack  = []
	for i in idx:
		stack.append([i])

	while len(stack)!=0:
		cur = stack.pop()

		for i in idx:
			if i not in cur:
				temp=cur+[i]
				if len(temp)==n:
					element = []
					for i in temp:
						element.append(lst[i])
					ret.append(element)
				else:
					stack.append(temp)
	return ret

from itertools import permutations
from itertools import combinations

import time

if __name__ == "__main__":
    items= [1,2,3,4]
    a = []
    start = time.time()
    for i in list(combinations(items,2)):
        a.append(i)
    print(a)
    print(time.time()-start)

    b = []
    start = time.time()
    for i in list(combinations(items,2)):
        b.append(i)
    print(b)
    print(time.time()-start)