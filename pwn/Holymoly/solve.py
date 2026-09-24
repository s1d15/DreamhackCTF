from pwn import *

HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

def ptr_inc(str):
    r.sendlineafter(b'? ', str)

ptr_inc(b'holymoly')
r.interactive()