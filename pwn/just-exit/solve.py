from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 11798
r = remote(HOST, PORT)

r.sendline(b'2 7 169')

r.interactive()