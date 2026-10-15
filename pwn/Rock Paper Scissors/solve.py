from pwn import *
from ctypes import CDLL

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13530
r = remote(HOST, PORT)

libc = CDLL('libc.so.6')
libc.srand(libc.time(0))
t = 'RPS'

for i in range(10):
    r.sendlineafter(b':', t[((libc.rand()%3)+1)%3].encode())

r.interactive()