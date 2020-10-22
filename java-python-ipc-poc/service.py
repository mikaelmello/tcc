import socket
import sys
import struct
import time

stdin = sys.stdin.buffer
stdout = sys.stdout.buffer
stderr = sys.stderr


def classify(inp):
    return 2


def read_floats(n):
    inp = []
    for i in range(n):
        b = stdin.read(4)
        f = struct.unpack("!f", b)
        inp.append(f)
    return inp


def server():
    while True:
        b = stdin.read(4)
        n = struct.unpack("!I", b)
        i = read_floats(n[0])

        res = classify(i)
        stdout.write(struct.pack("!B", res))
        stdout.flush()


if __name__ == "__main__":
    server()
