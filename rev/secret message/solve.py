with open('secretMessage.enc', 'rb') as f:
    with open('secretMessage.raw', 'wb') as r:
        prev=b''
        while True:
            curr = f.read(1)
            if curr == b'':
                break
            r.write(curr)
            if curr != prev:
                prev = curr
            else:
                curr = f.read(1)
                if curr == b'\x00':
                    continue
                else:
                    r.write(prev * curr[0])
