from pwn import *
from z3 import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12248
r = remote(HOST, PORT)

s = Solver()
year = Int('y')
month = IntVal(12)
s.add((year / -100 + year / 4 + 23 * month / 9 + (25+(year-2)) + 4 + year / 400) % 7 == 0)
s.add(year >= 100000000)
s.check()
m=s.model()
r.sendline(b'%d 12 25 23 59 59'%m[year].as_long())
r.interactive()