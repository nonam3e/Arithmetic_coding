import decimal
import hashlib

chunk_size = 128
num = 150


def print_hashsum(content):
    md5 = hashlib.md5()
    md5.update(content)
    print(f'Checksum: {md5.hexdigest()}')


def from_interval(a, b):
    counter = 8 * chunk_size
    c = 0
    cur_sum = 0
    prev = decimal.Decimal(1)
    for i in range(chunk_size * 8):
        num = cur_sum + prev / 2
        if num < a < b:
            c = c << 1 | 1
            cur_sum = num
        elif a < b <= num:
            c = c << 1
        else:
            c = c << 1 | 1
            c = c << counter - 1
            return c
        prev /= 2
        counter -= 1
    print("shit")
    raise BufferError


def from_bytes(a):
    n = 0
    a_copy = a
    while True:
        n += 1
        a_copy = a_copy >> 1
        if (a_copy & 1):
            break


    ans = 0
    prev = decimal.Decimal(1)
    for i in range(chunk_size * 8 - 1, n - 1, -1):
        prev /= 2
        if a >> i & 1:
            ans += prev
    return ans