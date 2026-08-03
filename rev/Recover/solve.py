key = b'\xde\xad\xbe\xef'

with open('encrypted', 'rb') as enc:
    file_bytes = enc.read()
    with open('flag.png', 'wb') as flag:
        for i in range(len(file_bytes)):
            flag.write((((file_bytes[i]-19)&0xff) ^ key[i%4]).to_bytes())