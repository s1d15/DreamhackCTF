data=bytearray(b'0+\x12\x06\x19N\x1d^F\x1dIR\t\x10@]@\\MNE\x15\n\r@S@TBRDZ^QF\x0cC\x19\x11\x12\x1cS]\x06H@\x10\x04\x1eM\x18_^FNT\x12^CLLFY]\x17X\x1b\x11{')

def xor(val):
    global data
    for i in range(0x45):
        data[i] ^= val[i%len(val)]

for x in (b'banana', b'strawberry', b'erwin', b'mandarin', b'melon'):
    xor(x)

print(''.join([chr(x) for x in data]))