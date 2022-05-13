import utils
import sys
import pathlib
import decimal


def decompress():
    raw = ''
    name = ''
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to decompress")
        exit()
    if pathlib.Path(name).suffix != ".bubylda":
        print("File hasn't been compressed yet")
        exit()
    body_size = pathlib.Path(name).stat().st_size
    # print(f"file size: {body_size}")
    alph_size = int.from_bytes(raw.read(1), "big")
    body_size -= 1
    counter = [0]
    symbols = []
    current_freq = 0
    for i in range(alph_size):
        symbols.append(raw.read(1))
        current_freq += int.from_bytes(raw.read(4), "big")
        counter.append(current_freq)
        body_size -= 5
    for i in range(alph_size + 1):
        counter[i] = decimal.Decimal(counter[i]) / current_freq
    print(counter)
    print(symbols)
    output = open(f"decompressed{pathlib.Path(name).stem}", "wb")
    while body_size != 0:
        point = int.from_bytes(raw.read(utils.chunk_size), "big") / decimal.Decimal(256 ** utils.chunk_size)
        chunk = 0
        while chunk < utils.num:
            chunk += 1
            start = binary_search(counter, point)
            if symbols[start] == b'\x03':
                break
            point = (point - counter[start]) / (counter[start + 1] - counter[start])
            output.write(symbols[start])
            print(symbols[start], end='')
        body_size -= utils.chunk_size
    output.close()
    raw.close()
    utils.print_hashsum(f"decompressed{pathlib.Path(name).stem}")


def binary_search(counter, num):
    low = 0
    high = len(counter) - 2
    while low <= high:
        middle = (low + high) // 2
        if counter[middle] <= num < counter[middle + 1]:
            return middle
        elif num < counter[middle]:
            high = middle - 1
        else:
            low = middle + 1
    raise ValueError


if __name__ == '__main__':
    decompress()
