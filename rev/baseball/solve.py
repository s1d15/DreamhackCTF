with open('text_in.txt', 'rb') as a:
    f_in = bytearray(a.read())

with open('text_out.txt', 'rb') as b:
    f_out = bytearray(b.read())

table = bytearray([0] * 64)

idx = 0
i = 0

while len(f_in) - i > 2:
    table[f_in[i] >> 2] = f_out[idx]
    table[(f_in[i+1]) >> 4 | (16 * f_in[i]) & 0x30] = f_out[idx+1]
    table[(f_in[i+2] >> 6) | (4 * f_in[i+1]) & 0x3c] = f_out[idx+2]
    table[f_in[i+2] & 0x3f] = f_out[idx+3]
    idx += 4
    i += 3

table[f_in[i] >> 2] = f_out[idx]
table[(f_in[i+1] >> 4) | (16 * f_in[i]) & 0x30] = f_out[idx+1]
table[(4 * f_in[i+1]) & 0x3c] = f_out[idx+2]

with open('table', 'wb') as t:
    t.write(table)

with open('flag_out.txt', 'rb') as c:
    encoded = bytearray(c.read())

flag_len = (40//4*3-2)
flag = []
i = 0

while flag_len - i > -5:
    flag.append(((table.index(encoded[i]) << 2) | (table.index(encoded[i+1]) >> 4)) & 0xff)
    flag.append(((table.index(encoded[i+1]) << 4) | (table.index(encoded[i+2]) >> 2)) & 0xff)
    flag.append(((table.index(encoded[i+2]) << 6) | (table.index(encoded[i+3]))) & 0xff)

    i += 4

flag.append(((table.index(encoded[i]) << 2) | (table.index(encoded[i+1]) >> 4)) & 0xff)
flag.append(((table.index(encoded[i+1]) << 4) | (table.index(encoded[i+2]) >> 2)) & 0xff)

print(''.join(chr(x) for x in flag))
        