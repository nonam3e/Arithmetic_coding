import hashlib
import pathlib
import decimal

chunk_size = 16
num = 20

def print_hashsum(content):
    md5 = hashlib.md5()
    md5.update(content)
    print(f'Checksum: {md5.hexdigest()}')

def from_interval(a,b):
def from_bytes(a):
