from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 12765
r = remote(HOST, PORT)

for i in range(50):
    eq = r.recvline().decode().strip('=?\n')
    r.sendline(str(eval(eq)).encode())
    
r.interactive()