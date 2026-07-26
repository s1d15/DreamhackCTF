from z3 import *

data = b'\xad\xd8\xcb\xcb\x9d\x97\xcb\xc4\x92\xa1\xd2\xd7\xd2\xd6\xa8\xa5\xdc\xc7\xad\xa3\xa1\x98L\x00'

s = Solver()
bv = [BitVec(f'c{i}', 8) for i in range(len(data)+1)]

for i in range(len(data)):
    s.add(BitVecVal(data[i], 8) == bv[i] + bv[i+1])

s.check()
m = s.model()

print(''.join([chr(m[bv[i]].as_long()) for i in range(len(data) + 1)]))