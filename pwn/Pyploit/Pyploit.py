#!/usr/bin/env python3.6

#-*- coding: utf-4 -*-

import random
import pdb

ML_A = [1, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999]

def Q_mod(x, d, n):
    y = x % n
    r = 1
    bd = bin(d)
    bd = bd[2:len(bd)]
    m = len(bd) - 1
    while (m != -1):
        if bd[m] == '1':
            r = r * y % n
        y = y ** 2 % n
        m = m - 1
    return r


def ML_test(n, a):
    d = (n - 1) // 2
    while (d % 2 == 0):
        if (pow(a, d, n) == n - 1):
            return True
        d = d // 2
    tmp = pow(a, d, n)
    if tmp == n - 1 or tmp == 1:
        return True
    else:
        return False


def F_test(n):
    a = 3
    if Q_mod(a, n - 1, n) == 1 or n == 3:
        return True
    else:
        return False


def prime_test(n):
    result = True
    if F_test(n):
        for x in ML_A:
            if not ML_test(n, x):
                result = False
                break
            if result:
                return True
    else:
        return False


def extended_euclid(r1, r2, s1=1, s2=0, t1=0, t2=1):
    q = r1 // r2
    s = s1 - s2 * q
    t = t1 - t2 * q
    r = r1 - r2 * q
    if (r == 0):
        res = {'gcd': r2, 's': s2, 't': t2}
        return res
    else:
        return extended_euclid(r2, r, s2, s, t2, t)


def find_d(e, Pn):
    res = extended_euclid(e, Pn)
    r = res['s']
    if r < 0:
        r = r + Pn
    return r


def gen_prime():
    N = random.randint(10 ** 127, 10 ** 128 - 1)
    while (not prime_test(N)):
        N = N + 1
    return N


def RSA():
    p = gen_prime()
    q = gen_prime()

    e = 65537

    Pn = (p - 1) * (q - 1)
    n = p * q

    d = find_d(e, Pn)

    return [e, d, n]


def encryption(a, e, n):
    return Q_mod(a, e, n)


def decryption(enc, d, n):
    return Q_mod(enc, d, n)

def enc_int(text):
    result = ''
    for i in range(0,len(text)):
        try:
            enc_code = str(int(text[i].encode('UTF-8').hex(),16))
        except:
            enc_code = str(int('?'.encode('UTF-8').hex(), 16))
        if len(enc_code) <5:
            enc_code = '0'*(5-len(enc_code)) + enc_code
        result = result + enc_code
    result = '1' + result
    return int(result)

def dec_int(code):
    code = str(code)
    result = ''
    code = code[1:len(code)]
    for i in range(0,len(code),5):
        try:
            rs = (bytes.fromhex(hex(int(code[i:i+5]))[2:])).decode('UTF-8')
        except:
            rs = '?'
        result = result + rs
    return result

def split_string(text):
    result = []
    if len(text) > 12:
        for i in range(0,len(text),12):
            result.append(text[i:i+12])
    else:
        return [text]
    return result

def trans_enc(text):
    text = split_string(text)
    result = ''
    for i in text:
        result = f'{result}/{encryption(enc_int(i),pub1,pub2)}'
    return result

def trans_dec(code):
    code = code.split('/')
    result = ''
    for i in range(1,len(code)):
        result = result + dec_int(decryption(int(code[i]),priv,pub2))
    return result

key = RSA()
pub1 = key[0]
pub2 = key[2]
priv = key[1]

def exit_():
    print('exit')
    exit()

def menu():
    print('1. Encrypt')
    print('2. Decrypt')
    print('3. Exit')

dict = {}

while(True):
    menu()
    print('index: ',end='')
    inp = input()

    if inp == '1':
        print('Text: ', end='')
        a = input()
        rs = trans_enc(a)
        dict[rs] = a
        print(rs)
    elif inp == '2':
        print('Code: ', end='')
        a = input()
        rs = trans_dec(a)
        print(rs)
        if a in dict:
            if dict[a] != rs:
                print('ERROR!')
                pdb.set_trace()

    else:
        exit_()



