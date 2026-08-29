from Crypto.Util.number import inverse

with open('out.bin', 'rb') as out:
    enc = out.read()

n = 4271010253
e = 201326609
p = 65287
q = 65419

phi=(p-1)*(q-1)
d = inverse(e, phi)

flag=b''
for i in range(len(enc) // 8):
    c = int.from_bytes(enc[i*8:i*8+8], 'little')
    m = pow(c, d, n)
    flag += m.to_bytes(4, 'little')

print(flag.decode('utf-8', errors='ignore'))
    