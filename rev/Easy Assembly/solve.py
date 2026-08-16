from z3 import *
from pwn import *

enc_flag = b'txKewH\\ih~\\ywbFyw\x05FTsrYih~\\~ZaWjwfZR\x02b\\yw\\\x00|W\r\rM'

s = Solver()
bv = [BitVec(f'c{i}', 8) for i in range(len(enc_flag))]

for i in range(len(enc_flag)):
    s.add(BitVecVal(enc_flag[i], 8) ^ BitVecVal(len(enc_flag), 8) ^ bv[i] == 0)

s.check()
m = s.model()
print(''.join([chr(m[bv[i]].as_long()) for i in range(len(enc_flag))]))