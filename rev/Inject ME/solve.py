
file_name = b'dreamhack.exe'
v9 = []

def ROL4(a, b):
    shift = a << b
    remaining = a >> (32-b)
    return (shift | remaining) & 0xffffffff


for i in range(0x10):
    v9.append(ROL4(int(file_name[:4][::-1].hex(), 16), i))

data = 0
data_2 = []
for i in range(16):
    data_2.append(v9[i])

def func():
    global data_2
    global data
    v2 = data_2[(data+13) & 0xf]
    v3 = ((v2 << 15) ^ v2 ^ (data_2[data] << 16) ^ data_2[data]) & 0xffffffff
    v1 = data_2[(data+9) & 0xf]
    data_2[data] = ((v1 >> 11) ^ v1 ^ v3) & 0xffffffff
    data = (data + 15) & 0xf
    data_2[data] ^= ((32 * ((v1 >> 11) ^ v1 ^ v3)) & 0xda442d24 ^ (((v1 >> 11) ^ v1) << 28) ^ (v1 >> 11) ^ v1 ^ (v3 << 18) ^ (4 * data_2[data])) & 0xffffffff
    return data_2[data]

for i in range(0x64):
    func()

v5 = 0x436E8879
v6 = 0x3080393E
v7 = 0x79FD35CC
v8 = 0xF50F300C

text = func() ^ 0x7ed39c88
v5 = func() ^  0x436e8879
v6 ^= func()
v7 ^= func()
v8 ^= func()

print(b''.join(v.to_bytes(4, 'little') for v in (text, v5, v6, v7, v8)))