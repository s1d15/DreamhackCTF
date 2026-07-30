from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 24142
r = remote(HOST, PORT)

val = int('a0b4c1d7'[::-1], 16)
r.recvuntil(b'number: ')
random_num = int(r.recvline().strip().decode(), 16)

r.sendlineafter(b'Input? ', str(random_num ^ val).encode())
r.interactive()