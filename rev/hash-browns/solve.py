import hashlib
import string

chars = string.printable

arr = [0xFE5D3A093968D02B, 0xBA0AA367C2862EAE, 0x8BEA2ADA9E26604F, 0x2E6F41C96DCF5224, 0x7FD91BD2949B75F3, 0x5B1ED8E6072F3A6, 0xC94045C6D4887611, 0x9D43DF6DF6B94D95, 0xB9A8A83C8AC08D80, 0x6D78E80376518464, 0xE81A20F2023C2D0, 0x2E41EAE69D89F186, 0x425C831DD2A3E5FD, 0x82788DBBDC4100EC, 0x6D0FEE8D3901DD20, 0xEBE82A0A41E5D783, 0x2AFA26414B72E506, 0xD1848E9C21D114D]

arr2 = [0 for i in range(9)]
cnt=0
for i in range(0, len(arr), 2):
    target=0
    for j in range(9):
        temp = (arr[i] >> 8*j) & 0xff
        target |= temp << 8*(8-j)
    target = target << 8*8
    for j in range(9):
        temp2 = (arr[i+1] >> 8*j) & 0xff
        target |= temp2 << 8*(8-j)
    target = target >> 8
    arr2[cnt] = target
    cnt+=1

flag = ''
for i in range(9):
    for x in chars:
        for y in chars:
            for z in chars:
                s = x+y+z
                val = int.from_bytes(hashlib.md5(s.encode()).digest(), byteorder='big')
                if val == arr2[i]:
                    flag += s
                    print(flag)
                    break