import string

def rot(a, b):
    return (((a&0xff) >> (b & 7)) | (a << (8 - (b & 7)))) & 0xff

def plus(a, b):
    return (a + b) & 0xff

def xor(a, b):
    return a ^ b

def operation(func, val, inp, len):
    for i in range(len):
        inp[i] = func(inp[i], val)

with open('program.bin', 'rb') as f:
    prog = f.read()

with open('output.bin', 'rb') as f:
    output = f.read()

prog = prog[2:]
flag = b''
for j in range(len(output)):
    for x in string.printable:
        inp = bytearray(x.encode())
        original = inp.copy()
        l = len(inp)
        for i in range(0, len(prog), 2):
            first, second = prog[i], prog[i+1]
            if first == 3:
                operation(rot, second, inp, l)
            elif first == 1:
                operation(plus, second, inp, l)
            elif first == 2:
                operation(xor, second, inp, l)
        if inp[0] == output[j]:
            flag += original
            break
print(flag)