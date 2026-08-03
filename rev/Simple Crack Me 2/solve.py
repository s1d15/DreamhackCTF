target = bytearray(b'\xf8\xe0\xe6\x9e\x7f2h1\x05\xdc\xa1\xaa\xaa\t\xb3\xd8A\xf06\x8c\xce\xc7\xacf\x91L2\xff\x05\xe0\xd9\x91')
data1 = b'\x113Uw\x99\xbb\xdd'
data2 = b'\xef\xbe\xad\xde'
data3 = b'\xde\xad\xbe\xef'

def func1(a, b):
    b_len = len(b)
    for i in range(0x20):
        a[i] = (a[i] ^ (b[i % b_len] & 0xff)) & 0xff
    return a

def func2(a, b):
    for i in range(0x20):
        a[i] = (a[i] - b) & 0xff
    return a

def func3(a, b):
    for i in range(0x20):
        a[i] = (a[i] + b) & 0xff
    return a

func1(target, data1)
func2(target, 243)
func3(target, 77)
func1(target, data2)
func3(target, 90)
func2(target, 31)
func1(target, data3)

print(''.join([chr(x) for x in target]))