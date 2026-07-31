from pwn import *

r = process('./simple_crack_me')
r.sendline(str(0x13371337).encode())
r.interactive()