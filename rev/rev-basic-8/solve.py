import string

data = b'\xac\xf3\x0c%\xa3\x10\xb7%\x16\xc6\xb7\xbc\x07%\x02\xd5\xc6\x11\x07\xc5\x00'

def func(c):
    return ord(c)*-5 & 0xff

for i in range(len(data)):
    for c in string.printable:
        if func(c) == data[i]:
            print(c,end='')
            break
print()
