import ida_bytes

b''.join([ida_bytes.get_bytes(0x401141+i,1) for i in range(0, 15*927, 15)])