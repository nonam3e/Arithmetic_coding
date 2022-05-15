import pathlib
import sys
import struct
import decimal
import utils


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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
    utils.print_hashsum(content)
    content += (3).to_bytes(1, byteorder="big")
    prob = {}
    counter = 0
    for item in content:
        letter = item.to_bytes(1, byteorder="big")
        if prob.get(letter) is None:
            prob[letter] = 1
        else:
            prob[letter] += 1
        counter += 1

    output = open(f"{pathlib.Path(name)}.bubylda", "wb")
    output.write((len(prob)%256).to_bytes(1, byteorder="big"))
    # prob = {k:v for k,v in sorted(prob.items(), key=lambda x: x[0])}
    decimal.getcontext().prec = 1000
    for key in prob:
        output.write(key)
        output.write(prob[key].to_bytes(4, byteorder="big"))
    for key in prob:
        prob[key] /= decimal.Decimal(counter)

    prob_id = {k: v for k, v in zip(prob.keys(), range(len(prob)))}
    prob = [v for v in prob.values()]
    for i in range(1, len(prob)):
        prob[i] += prob[i - 1]
    prob.insert(0, 0)
    prob[len(prob) - 1] = decimal.Decimal(1)
    # print(prob)
    # print(prob_id)
    start, end = decimal.Decimal(0), decimal.Decimal(1)
    chunk = 0
    result = 0
    cap = 256**utils.chunk_size

    for item in content:
        interval = end - start
        end = start + interval * prob[prob_id[item.to_bytes(1, byteorder="big")] + 1]
        start = start + interval * prob[prob_id[item.to_bytes(1, byteorder="big")]]
        chunk += 1
        if chunk == utils.num:
            chunk = 0
            result = utils.from_interval(start, end)
            output.write(result.to_bytes(utils.chunk_size, byteorder="big"))
            # print(result, end=' ')
            start, end = decimal.Decimal(0), decimal.Decimal(1)
    if chunk:
        result = int(cap * (end + start) / 2)
        output.write(result.to_bytes(utils.chunk_size, byteorder="big"))
        # print(result)
# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    compress()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
