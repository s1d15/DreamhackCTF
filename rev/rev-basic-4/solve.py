from z3 import *
data = '242713c6c61316e647f5269647f54627132626c656f5c3c3f5e3e300'
data = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
# 16 * user_input[i] | user_input[i] >> 4 != data[i]

s = Solver()
bv = [BitVec(f'c{i}', 8) for i in range(len(data))]

for i in range(len(data)):
    s.add(BitVecVal(data[i], 8) == BitVecVal(16, 8)  * (bv[i] & 0xff) | bv[i] >> BitVecVal(4, 8))

s.check()
m = s.model()

print(''.join([chr(m[bv[i]].as_long()) for i in range(len(data))]))