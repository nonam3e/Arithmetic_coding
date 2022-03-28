import pathlib
import sys


# struct: dict len (1), dict (len){index(1),value len(1),value(len)},
# len of power (1), power of 10 (len),len of data (1), data (size-previous)
def int_to_bytes(x):
    length = (x.bit_length() + 7) // 8
    if length == 0:
        length += 1
    return length.to_bytes(1, 'big') + x.to_bytes(length, 'big')
def int_bytes(x):
    length = (x.bit_length() + 7) // 8
    if length == 0:
        length += 1
    return x.to_bytes(length, 'big')

def fast_power(base, power):
    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * base)
        power = power // 2
        base = (base * base)
    return result


def compress():
    name = ''
    raw = ''
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to compress")
        exit()
    if pathlib.Path(name).suffix == ".bubylda":
        print("File has already been compressed")
        exit()
    content = raw.read()
    content += (3).to_bytes(1, byteorder="big")
    frequency = {}
    counter = 0
    for item in content:
        letter = item.to_bytes(1, byteorder="big")
        if frequency.get(letter) is None:
            frequency[letter] = 1
        else:
            frequency[letter] += 1
        counter += 1

    output = open(f"{pathlib.Path(name)}.bubylda", "wb")
    output.write(len(frequency).to_bytes(1, byteorder="big"))
    frequency = {k: v for k, v in sorted(frequency.items(), key=lambda x: x[0])}
    frequency_id = {k: v for k, v in zip(range(len(frequency)), frequency.keys())}
    frequency_reverse_id = {v: k for k, v in zip(range(len(frequency)), frequency.keys())}
    frequency = [v for v in frequency.values()]
    cumulative_freq = {frequency_id[0]: 0}
    output.write(frequency_id[0])
    output.write(int_to_bytes(cumulative_freq[frequency_id[0]]))
    for i in range(1, len(frequency)):
        cumulative_freq[frequency_id[i]] = cumulative_freq[frequency_id[i - 1]] + frequency[i - 1]
        output.write(frequency_id[i])
        output.write(int_to_bytes(cumulative_freq[frequency_id[i]]))
    print(cumulative_freq)
    product_freq = 1
    l_bound = 0
    for item in content:
        l_bound += l_bound * counter + cumulative_freq[item.to_bytes(1, byteorder="big")] * product_freq
        product_freq *= frequency[frequency_reverse_id[item.to_bytes(1, byteorder="big")]]
    u_bound = l_bound + product_freq
    print(f"L: {l_bound}\nU: {u_bound}")
    dec_power = 0
    sub = u_bound - l_bound
    while sub >= 10:
        sub //= 10
        dec_power += 1
    u_bound //= fast_power(10, dec_power)
    print(f"F: {u_bound * 10 ** dec_power}")
    output.write(int_to_bytes(dec_power))
    output.write(int_bytes(u_bound))


if __name__ == '__main__':
    compress()
