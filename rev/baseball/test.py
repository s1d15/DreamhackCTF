from pathlib import Path

f_in = bytearray(Path("text_in.txt").read_bytes())
f_out = bytearray(Path("text_out.txt").read_bytes().strip())
encoded = bytearray(Path("flag_out.txt").read_bytes().strip())

table = bytearray([0] * 64)

idx = 0
i = 0

while len(f_in) - i > 2:
    b0 = f_in[i]
    b1 = f_in[i + 1]
    b2 = f_in[i + 2]

    table[b0 >> 2] = f_out[idx]
    table[(b1 >> 4) | ((b0 << 4) & 0x30)] = f_out[idx + 1]
    table[(b2 >> 6) | ((b1 << 2) & 0x3c)] = f_out[idx + 2]
    table[b2 & 0x3f] = f_out[idx + 3]

    idx += 4
    i += 3

remaining = len(f_in) - i

if remaining == 1:
    b0 = f_in[i]
    table[b0 >> 2] = f_out[idx]
    table[(b0 << 4) & 0x30] = f_out[idx + 1]

elif remaining == 2:
    b0 = f_in[i]
    b1 = f_in[i + 1]

    table[b0 >> 2] = f_out[idx]
    table[(b1 >> 4) | ((b0 << 4) & 0x30)] = f_out[idx + 1]
    table[(b1 << 2) & 0x3c] = f_out[idx + 2]

print("missing table indexes:", [i for i, c in enumerate(table) if c == 0])

inv = {c: i for i, c in enumerate(table) if c != 0}

flag = bytearray()

for i in range(0, len(encoded), 4):
    c0, c1, c2, c3 = encoded[i:i+4]

    n0 = inv[c0]
    n1 = inv[c1]

    flag.append((n0 << 2) | (n1 >> 4))

    if c2 == ord("="):
        break

    n2 = inv[c2]
    flag.append(((n1 & 0xf) << 4) | (n2 >> 2))

    if c3 == ord("="):
        break

    n3 = inv[c3]
    flag.append(((n2 & 0x3) << 6) | n3)

print(flag.decode())