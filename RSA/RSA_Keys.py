# coding=utf-8
# @Time    : 2022/5/21 19:45
# @Author  : Nisky
# @File    : RSA_Keys.py
# @Software: PyCharm
from random import randint


# Miller Rabin算法
def miller_rabin(p):
    if p == 1:
        return False
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    m, k, = p - 1, 0
    while m % 2 == 0:
        m, k = m // 2, k + 1
    a = randint(2, p - 1)
    x = pow(a, m, p)
    if x == 1 or x == p - 1:
        return True
    while k > 1:
        x = pow(x, 2, p)
        if x == 1:
            return False
        if x == p - 1:
            return True
        k = k - 1
    return False


# 40轮素性检测
def is_prime(p, r=40):
    for i in range(r):
        if not miller_rabin(p):
            return False
    return True


# 扩展欧几里得
def EX_GCD(a, b, arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = EX_GCD(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - int(a // b) * arr[1]
    return g


# ax=1(mod n) 求a模n的乘法逆x
def ModReverse(a, n):
    arr = [0, 1, ]
    gcd = EX_GCD(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1


def create_keys():
    PN = []
    index = 1024
    for _ in range(2):
        num = 0
        for i in range(index):
            num = num * 2 + randint(0, 1)
        while not is_prime(num):
            num = num + 1
        PN.append(num)
    p = PN[0]
    q = PN[1]
    n = p * q
    f = (p - 1) * (q - 1)
    e = 65537
    arr = [0, 1, ]
    d = ModReverse(e, f)
    result = [n, e, d]
    return result


if __name__ == '__main__':
    print(create_keys())
