from z3 import *

s = Solver()

bv = [BitVec(f'c{i}', 8) for i in range(64)]
rot = [(bv[i] + 13) & 0x7f for i in range(64)]
target = b'C@qpl==Bppl@<=pG<>@l>@Blsp<@l@AArqmGr=B@A>q@@B=GEsmC@ArBmAGlA=@q'

for i in range(64):
    s.add((rot[63-i] ^ 3) == target[i])

s.check()
m = s.model()

print(''.join([chr(m[bv[i]].as_long()) for i in range(len(bv))]))