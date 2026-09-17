import math

lst=[]
for i in range(1, 81):
    for j in range(1000, 900, -1):
        res = int(math.ceil(j/i)*i)
        print(i, int(math.ceil(j/i)*i))
        if res > 1000:
            lst.append((res, i, j))

print(sorted(lst))