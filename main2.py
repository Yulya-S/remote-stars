import socket
import matplotlib.pyplot as plt
import numpy as np


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

host = "84.237.21.36"
port = 5152

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)

        im = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        pos1 = np.unravel_index(np.argmax(im), im.shape)
        n = 0
        for i in range(pos1[1], pos1[1] + len(im[pos1[0], pos1[1]:])):
            if im[pos1[0], i] == 0:
                break
            im[pos1[0], i] = 0
            n += 1
        im[pos1[0] - (n + 1): pos1[0] + n + 1, pos1[1] - (n + 1):pos1[1] + (n + 1)] = 0
        pos2 = np.unravel_index(np.argmax(im), im.shape)

        res = round(np.sqrt((pos2[1]-pos1[1]) ** 2 + (pos2[0]-pos1[0]) ** 2), 1)

        sock.send(f"{res}".encode())
        print(sock.recv(4), res)

        sock.send(b"beat")
        beat = sock.recv(20)