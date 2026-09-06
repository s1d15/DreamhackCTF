from pwn import *

HOST, PORT = '0.0.0.0', 31337
r = process('./chall')

'''
Patched the following:
    - Removed sleep(seconds)
    - Since 1st `if rand() % 10 == 5`
        -> At 1st `if: rand() % 10 != seconds` and
        -> `v8[i] = get_flag((unsigned int)*((char *)v6 + i), 5);`
Then test from 0 to 9 -> 2nd if rand() % 10 == 3
'''
r.sendline(b'3')
r.interactive()