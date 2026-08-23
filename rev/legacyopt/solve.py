from pwn import *
import string

HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

enc='220c6a33204455fb390074013c4156d704316528205156d70b217c14255b6ce10837651234464e'
enc=[enc[i:i+2] for i in range(0, len(enc), 2)]
flag=''
idx=0
for i in range(39):
    for x in string.ascii_letters + '_\{\}' + string.digits:
        r=remote(HOST, PORT)
        payload=flag+x
        r.sendline(payload.ljust(39,'A').encode())
        res=r.recvline().decode().strip()
        if res[idx:idx+2] == enc[i]:
            flag+=x
            idx+=2
            break 
print(flag)
r.interactive()