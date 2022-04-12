import pathlib
import sys
import struct
import decimal


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Segment:
    def __init__(self, left: decimal.Decimal = 0, right: decimal.Decimal = 0):
        self.left = left
        self.right = right

    def __str__(self):
        result = f"[{self.left};{self.right})"
        return result


def start_position():
    segments = []
    prob = decimal.Decimal(1) / 256
    left = decimal.Decimal(0)
    right = prob
    for i in range(256):
        segments.append(Segment(left, right))
        left = right
        right += prob
    return segments


def new_position(segments, weights):
    sum = decimal.Decimal(0)
    for i in range(256):
        sum += weights[i]
    left = decimal.Decimal(0)
    for i in range(256):
        segments[i] = Segment(left, left + (weights[i]) / sum)
        left = segments[i].right
    return segments


def compress():
    segments = start_position()
    weights = [1] * 256
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
    output = open(f"{pathlib.Path(name)}.bubylda", "wb")

    chunk_size = 4
    left, right = decimal.Decimal(0), decimal.Decimal(1)
    chunk = 0
    for item in content:
        weights[int(item)] += 1
        left, right = left + (right - left) * segments[int(item)].left, \
                      left + (right - left) * segments[int(item)].right
        new_position(segments, weights)
        chunk += 1
        if chunk==3:
            chunk = 0
            result = int(256**chunk_size * (left + right) / 2)
            output.write(result.to_bytes(chunk_size, byteorder="big"))
            print(f"{256**chunk_size * left}____{256**chunk_size * right}")
            left, right = decimal.Decimal(0), decimal.Decimal(1)
    print((left + right)/2)
    output.write(struct.pack("d", (left + right)/2))



# def compress():
#     name = ''
#     raw = ''
#     try:
#         name = sys.argv[1]
#         raw = open(name, "rb")
#     except IndexError:
#         print("Choose file to compress")
#         exit()
#     if pathlib.Path(name).suffix == ".bubylda":
#         print("File has already been compressed")
#         exit()
#     content = raw.read()
#     content += (3).to_bytes(1, byteorder="big")
#     prob = {}
#     counter = 0
#     for item in content:
#         letter = item.to_bytes(1, byteorder="big")
#         if prob.get(letter) is None:
#             prob[letter] = 1
#         else:
#             prob[letter] += 1
#         counter += 1
#
#     output = open(f"{pathlib.Path(name)}.bubylda", "wb")
#     output.write((len(prob) % 256).to_bytes(1, byteorder="big"))
#     # prob = {k:v for k,v in sorted(prob.items(), key=lambda x: x[0])}
#     decimal.getcontext().prec = 10
#
#     # for key in prob:
#     #     output.write(key)
#     #     output.write(prob[key].to_bytes(4, byteorder="big"))
#     # for key in prob:
#     #     prob[key] /= decimal.Decimal(counter)
#
#     prob_id = {k: v for k, v in zip(prob.keys(), range(len(prob)))}
#     prob = [v for v in prob.values()]
#     for i in range(1, len(prob)):
#         prob[i] += prob[i - 1]
#     prob.insert(0, 0)
#     prob[len(prob) - 1] = decimal.Decimal(1)
#     print(prob)
#     print(prob_id)
#     chunk_size = 2048
#     start, end = decimal.Decimal(0), decimal.Decimal(1)
#     chunk = 0
#     result = 0
#     for item in content:
#         interval = end - start
#         end = start + interval * prob[prob_id[item.to_bytes(1, byteorder="big")] + 1]
#         start = start + interval * prob[prob_id[item.to_bytes(1, byteorder="big")]]
#         chunk += 1
#         if chunk == 2:
#             chunk = 0
#             result = int(chunk_size * (end + start) / 2) + 1
#             output.write(result.to_bytes(chunk_size // 256, byteorder="big"))
#             print(result)
#             start, end = decimal.Decimal(0), decimal.Decimal(1)
#     if chunk:
#         result = int(chunk_size * (end + start) / 2)
#         output.write(result.to_bytes(chunk_size // 256, byteorder="big"))
#         print(result)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    compress()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
