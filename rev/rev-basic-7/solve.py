from z3 import *
data = b'R\xdf\xb3`\xf1\x8b\x1c\xb5W\xd1\x9f8K)\xd9&\x7f\xc9\xa3\xe9S\x18O\xb8j\xcb\x87X[9\x1e'

s = Solver()
bv = [BitVec(f'c{i}', 8) for i in range(len(data))]

for i in range(len(data)):
    s.add(BitVecVal(data[i], 8) == i ^ (bv[i] << (i&7) | (bv[i] >> (8 - (i&7)))))

s.check()
m = s.model()

print(''.join([chr(m[bv[i]].as_long()) for i in range(len(data))]))