import hashlib
import pathlib


def print_hashsum(content):
    try:
        pathlib.Path(content).is_file()
        content = open(content, "rb").read()
    except TypeError:
        if isinstance(content, bytes):
            pass
    finally:
        md5 = hashlib.md5()
        md5.update(content)
        print(f'Checksum: {md5.hexdigest()}')
