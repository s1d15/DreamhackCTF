enc_flag = b'IM{508889j32j87j9jg54650840428hjhi2ii08h74ihj538h543j7g6k5jk8jih22f}'
real_flag = [b''] * len(enc_flag)
val5 = 5

v10 = b'abcdefghijklmnopqrstuvwxyz'
v9 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
v8 = [b''] * 64

for i in range(26):
    v8[(val5 + i) % 26 + 32] = v10[i]
    v8[(val5+i) % 26] = v9[i]

v8[i+32]=0
v8[i]=0

for j in range(len(enc_flag)):
    v11 = chr(enc_flag[j])
    if v11.isupper():
        real_flag[j] = v8[ord(v11)-65]
    elif v11.islower():
        real_flag[j] = v8[ord(v11)-65]
    elif v11.isdigit():
        v14 = (val5+3) * ord(v11) % 9
        if (v14 <= 7 or v14 > 9):
            v14 += 50
        else:
            v14 += 40
        real_flag[j] = v14
    else:
        real_flag[j] = ord(v11)


print(''.join([chr(x) for x in real_flag]))
